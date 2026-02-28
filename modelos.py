from enum import Enum
from dataclasses import dataclass, field
from typing import Optional
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TipoProfesional(Enum):
    INGENIERO_ML = "ingeniero_ml"
    DATA_SCIENTIST = "data_scientist"
    SOFTWARE_ENGINEER_AI = "software_engineer_ai"
    FULLSTACK_DEVELOPER = "fullstack_developer"
    EXPERTO_CIBERSEGURIDAD = "experto_ciberseguridad"
    FRONTEND_DEVELOPER = "frontend_developer"
    BACKEND_DEVELOPER = "backend_developer"


class MetodoEvaluacion(Enum):
    ESTRUCTURADO = "estructurado"
    LANGCHAIN = "langchain"


@dataclass
class RequisitosPuesto:
    stack_tecnico: list[str]
    nivel_solicitado: str
    experiencia_minima_anios: int
    habilidades_blandas: list[str] = field(default_factory=list)


@dataclass
class ResultadoEvaluacion:
    porcentaje_match: float
    seniority_estimado: str
    brechas_tecnicas: list[str]
    skills_encontradas: list[str]
    skills_faltantes: list[str]
    nivel_coherente: bool
    resumen_evaluacion: str

    def to_json(self) -> str:
        return json.dumps(
            {
                "porcentaje_match": self.porcentaje_match,
                "seniority_estimado": self.seniority_estimado,
                "brechas_tecnicas": self.brechas_tecnicas,
                "skills_encontradas": self.skills_encontradas,
                "skills_faltantes": self.skills_faltantes,
                "nivel_coherente": self.nivel_coherente,
                "resumen_evaluacion": self.resumen_evaluacion,
            },
            indent=2,
            ensure_ascii=False,
        )


@dataclass
class TrazabilidadAgente:
    agente: str
    status: str
    duracion_ms: float
    input_data: dict
    output_data: dict
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "agente": self.agente,
            "status": self.status,
            "duracion_ms": self.duracion_ms,
            "input": self.input_data,
            "output": self.output_data,
            "error": self.error,
        }


@dataclass
class ResultadoCompleto:
    resultado: ResultadoEvaluacion
    trazabilidad: list[TrazabilidadAgente]
    metodo: str
    timestamp: str

    def to_json(self) -> str:
        return json.dumps(
            {
                "resultado": {
                    "porcentaje_match": self.resultado.porcentaje_match,
                    "seniority_estimado": self.resultado.seniority_estimado,
                    "brechas_tecnicas": self.resultado.brechas_tecnicas,
                    "skills_encontradas": self.resultado.skills_encontradas,
                    "skills_faltantes": self.resultado.skills_faltantes,
                    "nivel_coherente": self.resultado.nivel_coherente,
                    "resumen_evaluacion": self.resultado.resumen_evaluacion,
                },
                "trazabilidad": [t.to_dict() for t in self.trazabilidad],
                "metodo": self.metodo,
                "timestamp": self.timestamp,
            },
            indent=2,
            ensure_ascii=False,
        )
