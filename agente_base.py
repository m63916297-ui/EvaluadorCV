from abc import ABC, abstractmethod
from typing import Any, Dict
from dataclasses import dataclass, field
from datetime import datetime
import time
import logging

from modelos import TrazabilidadAgente

logger = logging.getLogger(__name__)


@dataclass
class PromptEstructurado:
    system_prompt: str
    user_template: str

    def construir(self, **kwargs) -> str:
        return self.user_template.format(**kwargs)


class AgenteBase(ABC):
    """Clase base para todos los agentes"""

    def __init__(self, nombre: str, llm_client):
        self.nombre = nombre
        self.llm = llm_client
        self.trazabilidad: list[TrazabilidadAgente] = []

    @abstractmethod
    def ejecutar(self, input_data: dict) -> dict:
        """Ejecuta la logica del agente"""
        pass

    def _ejecutar_con_trazabilidad(self, input_data: dict) -> dict:
        """Ejecuta el agente con medicion de tiempo y trazabilidad"""
        inicio = time.time()
        output = {}
        error = None

        try:
            logger.info(f"[{self.nombre}] Iniciando ejecucion")
            output = self.ejecutar(input_data)
            logger.info(f"[{self.nombre}] Ejecucion completada")
        except Exception as e:
            logger.error(f"[{self.nombre}] Error: {e}")
            error = str(e)
            output = {"error": error}

        duracion = (time.time() - inicio) * 1000

        trazabilidad = TrazabilidadAgente(
            agente=self.nombre,
            status="error" if error else "success",
            duracion_ms=round(duracion, 2),
            input_data=input_data,
            output_data=output,
            error=error,
        )
        self.trazabilidad.append(trazabilidad)

        return output


PROMPTS = {
    "analista_skills": PromptEstructurado(
        system_prompt="""Eres un analizador de CVs experto. Tu tarea es extraer habilidades tecnicas y blandas mencionadas en un curriculum vitae.
        
Debes identificar:
1. Lenguajes de programacion
2. Frameworks y librerias
3. Bases de datos
4. Herramientas cloud y DevOps
5. Metodologias
6. Habilidades blandas

Responde en formato JSON con la siguiente estructura:
{
  "skills_tecnicas": ["skill1", "skill2", ...],
  "skills_blandas": ["skill1", "skill2", ...],
  "experiencia_anios": numero,
  "nivel_autodetectado": "nivel detectado en el CV"
}""",
        user_template="""Analiza el siguiente CV y extrae las habilidades:

CV:
{cv_texto}

Responde SOLO con JSON valido.""",
    ),
    "evaluador_seniority": PromptEstructurado(
        system_prompt="""Eres un evaluador de perfiles tecnicos especializado en determinar niveles de seniority.

Niveles de seniority:
- junior: 0-2 anos, requiere supervision
- semi-senior: 2-4 anos, trabajo autonomo
- senior: 4-7 anos, liderazgo tecnico
- staff: 7-10 anos, liderazgo de equipos
- principal: 10+ anos, estrategia tecnica

Responde en JSON:
{
  "seniority_estimado": "nivel",
  "experiencia_detectada": numero,
  "fundamento": "explicacion breve",
  "coherente": true/false,
  "indicadores_encontrados": []
}""",
        user_template="""Evalua el seniority de este candidato:

CV:
{cv_texto}

Nivel solicitado: {nivel_solicitado}
Experiencia minima requerida: {exp_minima} anos

Responde SOLO con JSON valido.""",
    ),
    "detector_brechas": PromptEstructurado(
        system_prompt="""Eres un analista de brechas tecnicas. Tu funcion es identificar las habilidades que faltan en un CV respecto a los requisitos del puesto.

Analiza:
1. Skills tecnicas que faltan
2. Skills que son criticas vs deseables
3. Posibilidad de cubrir brechas con experiencia

Responde en JSON:
{
  "brechas_criticas": ["skill1", ...],
  "brechas_deseables": ["skill1", ...],
  "skills_coincidentes": ["skill1", ...],
  "evaluacion_global": "descripcion breve"
}""",
        user_template="""Detecta las brechas entre este CV y los requisitos:

CV:
{cv_texto}

Stack requerido: {stack_requerido}

Responde SOLO con JSON valido.""",
    ),
    "calculador_match": PromptEstructurado(
        system_prompt="""Eres un calculador de compatibilidad entre candidatos y puestos.

Calculos a realizar:
1. Match tecnico: % de skills que coinciden
2. Match de seniority: compatibilidad de niveles
3. Ajuste por brechas: penalizacion por skills faltantes
4. Score final: combinacion ponderada

Ponderacion:
- Match tecnico: 70%
- Match seniority: 30%

Responde en JSON:
{
  "porcentaje_match": numero,
  "match_tecnico": numero,
  "match_seniority": numero,
  "clasificacion": "excelente/bueno/regular/bajo/no_recomendado",
  "resumen": "descripcion breve"
}""",
        user_template="""Calcula el porcentaje de match:

Skills del candidato: {skills_encontradas}
Skills requeridas: {stack_requerido}
Nivel estimado: {seniority_estimado}
Nivel requerido: {nivel_solicitado}
Brechas: {brechas}

Responde SOLO con JSON valido.""",
    ),
}
