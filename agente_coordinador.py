from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field
import logging

from modelos import (
    ResultadoEvaluacion,
    ResultadoCompleto,
    TrazabilidadAgente,
    RequisitosPuesto,
)
from llm_client import LLMClient, create_llm_client
from agentes_especializados import (
    AgenteAnalistaSkills,
    AgenteEvaluadorSeniority,
    AgenteDetectorBrechas,
    AgenteCalculadorMatch,
)
from reglas import ReglasEvaluacion, get_clasificacion

logger = logging.getLogger(__name__)


@dataclass
class ConfiguracionEvaluacion:
    """Configuracion para la evaluacion"""

    api_key: Optional[str] = None
    modelo: str = "gpt-4"
    usar_langchain: bool = True
    incluir_trazabilidad: bool = True


class AgenteCoordinador:
    """
    Agente Coordinador - Orquestra el flujo de evaluacion de CVs

    Responsabilidades:
    1. Inicializar agentes especializados
    2. Gestionar flujo de datos entre agentes
    3. Manejar errores y trazabilidad
    4. Consolidar resultados

    Arquitectura:
    ┌──────────────────────────────────────────────────────┐
    │              AgenteCoordinador                        │
    │  (Orquestacion y flujo)                              │
    └──────────────────────┬───────────────────────────────┘
                           │
    ┌──────────────────────┼───────────────────────────────┐
    │                      │                               │
    v                      v                               v
    ┌────────────┐   ┌────────────┐              ┌────────────┐
    │ Analista   │-> │ Evaluador  │   ->        │ Detector   │
    │ Skills     │   │ Seniority  │              │ Brechas    │
    └────────────┘   └────────────┘              └─────┬──────┘
                                                      │
                                                      v
                                              ┌────────────┐
                                              │ Calculador │
                                              │ Match      │
                                              └────────────┘
    """

    def __init__(self, config: Optional[ConfiguracionEvaluacion] = None):
        self.config = config or ConfiguracionEvaluacion()
        self.llm = create_llm_client(
            api_key=self.config.api_key, model=self.config.modelo
        )

        self.agentes = {
            "analista_skills": AgenteAnalistaSkills(self.llm),
            "evaluador_seniority": AgenteEvaluadorSeniority(self.llm),
            "detector_brechas": AgenteDetectorBrechas(self.llm),
            "calculador_match": AgenteCalculadorMatch(self.llm),
        }

        self.trazabilidad_global: list[TrazabilidadAgente] = []
        logger.info("AgenteCoordinador inicializado")

    def evaluar(
        self,
        cv_texto: str,
        stack_requerido: list[str],
        nivel_solicitado: str,
        experiencia_minima: int = 0,
        habilidades_blandas: list[str] = None,
    ) -> ResultadoCompleto:
        """
        Ejecuta el flujo completo de evaluacion

        Flujo:
        1. AnalistaSkills -> Extrae skills del CV
        2. EvaluadorSeniority -> Determina nivel
        3. DetectorBrechas -> Identifica gaps
        4. CalculadorMatch -> Calcula compatibilidad
        """
        inicio_total = datetime.now()
        logger.info(f"Iniciando evaluacion de CV")

        try:
            resultado_analisis = self._ejecutar_agente(
                "analista_skills", {"cv_texto": cv_texto}
            )

            resultado_seniority = self._ejecutar_agente(
                "evaluador_seniority",
                {
                    "cv_texto": cv_texto,
                    "nivel_solicitado": nivel_solicitado,
                    "experiencia_minima": experiencia_minima,
                },
            )

            resultado_brechas = self._ejecutar_agente(
                "detector_brechas",
                {
                    "skills_encontradas": resultado_analisis.get("skills_tecnicas", []),
                    "stack_requerido": stack_requerido,
                    "cv_texto": cv_texto,
                },
            )

            resultado_match = self._ejecutar_agente(
                "calculador_match",
                {
                    "skills_encontradas": resultado_brechas.get(
                        "skills_coincidentes", []
                    ),
                    "stack_requerido": stack_requerido,
                    "seniority_estimado": resultado_seniority.get(
                        "seniority_estimado", "senior"
                    ),
                    "nivel_solicitado": nivel_solicitado,
                    "brechas_criticas": resultado_brechas.get("brechas_criticas", []),
                },
            )

            resultado = ResultadoEvaluacion(
                porcentaje_match=resultado_match.get("porcentaje_match", 0),
                seniority_estimado=resultado_seniority.get(
                    "seniority_estimado", "senior"
                ),
                brechas_tecnicas=resultado_brechas.get("brechas_criticas", []),
                skills_encontradas=resultado_brechas.get("skills_coincidentes", []),
                skills_faltantes=resultado_brechas.get("brechas_criticas", []),
                nivel_coherente=resultado_seniority.get("coherente", True),
                resumen_evaluacion=resultado_match.get("resumen", ""),
            )

            self.trazabilidad_global.extend(
                [t for agente in self.agentes.values() for t in agente.trazabilidad]
            )

            return ResultadoCompleto(
                resultado=resultado,
                trazabilidad=self.trazabilidad_global,
                metodo="langchain" if self.config.usar_langchain else "estructurado",
                timestamp=inicio_total.isoformat(),
            )

        except Exception as e:
            logger.error(f"Error en evaluacion: {e}")
            return self._crear_resultado_error(str(e), inicio_total)

    def _ejecutar_agente(self, nombre: str, input_data: dict) -> dict:
        """Ejecuta un agente y maneja errores"""
        try:
            agente = self.agentes[nombre]
            return agente._ejecutar_con_trazabilidad(input_data)
        except Exception as e:
            logger.error(f"Error en agente {nombre}: {e}")
            return {"error": str(e)}

    def _crear_resultado_error(self, error: str, inicio: datetime) -> ResultadoCompleto:
        """Crea un resultado de error"""
        resultado = ResultadoEvaluacion(
            porcentaje_match=0,
            seniority_estimado="desconocido",
            brechas_tecnicas=[],
            skills_encontradas=[],
            skills_faltantes=[],
            nivel_coherente=False,
            resumen_evaluacion=f"Error en evaluacion: {error}",
        )

        return ResultadoCompleto(
            resultado=resultado,
            trazabilidad=self.trazabilidad_global,
            metodo="error",
            timestamp=inicio.isoformat(),
        )

    def obtener_trazabilidad(self) -> list[TrazabilidadAgente]:
        """Retorna la trazabilidad de la ultima evaluacion"""
        return self.trazabilidad_global

    def limpiar_trazabilidad(self):
        """Limpia la trazabilidad"""
        self.trazabilidad_global = []
        for agente in self.agentes.values():
            agente.trazabilidad = []


def crear_coordinador(api_key: Optional[str] = None) -> AgenteCoordinador:
    """Factory para crear el coordinador"""
    config = ConfiguracionEvaluacion(
        api_key=api_key, usar_langchain=api_key is not None
    )
    return AgenteCoordinador(config)
