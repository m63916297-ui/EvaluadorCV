"""
Workflows y Reglas de Configuración para el Evaluador de CV

Este módulo define los flujos de trabajo, reglas de evaluación
y configuraciones para los agentes.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional


class MetodoEvaluacion(Enum):
    ESTRUCTURADO = "estructurado"  # Análisis basado en reglas
    LANGCHAIN = "langchain"  # Usando LangChain Agent
    CREW_AI = "crew_ai"  # Múltiples agentes Crew


@dataclass
class ReglasEvaluacion:
    peso_match_tecnico: float = 0.70
    peso_match_seniority: float = 0.30
    umbral_excelente: float = 80.0
    umbral_bueno: float = 60.0
    umbral_regular: float = 40.0
    penalizacion_brecha: float = 0.10
    max_brechas_aceptables: int = 2


WORKFLOW_DEFAULT = {
    "pasos": [
        {
            "orden": 1,
            "agente": "AgenteAnalizadorSkills",
            "descripcion": "Extraer skills del CV",
            "obligatorio": True,
            "timeout": 30,
        },
        {
            "orden": 2,
            "agente": "AgenteEvaluadorSeniority",
            "descripcion": "Evaluar nivel de seniority",
            "obligatorio": True,
            "timeout": 20,
        },
        {
            "orden": 3,
            "agente": "AgenteDetectorBrechas",
            "descripcion": "Identificar brechas técnicas",
            "obligatorio": True,
            "timeout": 25,
        },
        {
            "orden": 4,
            "agente": "AgenteCalculadorMatch",
            "descripcion": "Calcular porcentaje de match",
            "obligatorio": True,
            "timeout": 15,
        },
    ],
    "fallback": {"si_falla": "usar_metodo_backup", "metodo_backup": "estructurado"},
}

WORKFLOW_LANGCHAIN = {
    "pasos": [
        {
            "orden": 1,
            "agente": "AgenteLangChain",
            "descripcion": "Análisis completo con LangChain",
            "obligatorio": True,
            "timeout": 60,
            "tools": ["ExtraerSkills", "EvaluarSeniority", "DetectarBrechas"],
        }
    ],
    "prompt_sistema": """Eres un evaluador experto de candidatos técnicos.
Analizas CVs y evalúas:
- Skills técnicos
- Nivel de seniority
- Compatibilidad con requisitos
- Brechas técnicas

Siempre respondes en JSON válido.""",
}

WORKFLOW_CREW = {
    "agentes": [
        {
            "nombre": "analista_skills",
            "rol": "Analista Técnico",
            "descripcion": "Extrae y cataloga habilidades técnicas",
            "objetivo": "Identificar todas las skills mencionadas",
        },
        {
            "nombre": "evaluador_seniority",
            "rol": "Evaluador de Perfil",
            "descripcion": "Determina nivel profesional",
            "objetivo": "Estimar seniority apropiado",
        },
        {
            "nombre": "detector_brechas",
            "rol": "Analista de Gap",
            "descripcion": "Identifica diferencias",
            "objetivo": "Listar skills faltantes",
        },
    ],
    "proceso": "sequential",
    "output": "consolidado",
}

REGLAS_SENIORITY = {
    "junior": {
        "rango_anios": (0, 2),
        "caracteristicas": ["trainee", "junior", "entry", "practicante"],
        "expectativas": ["requiere_supervision", "aprendizaje_activo"],
    },
    "semi-senior": {
        "rango_anios": (2, 4),
        "caracteristicas": ["semi senior", "semi-senior", "mid-level"],
        "expectativas": ["trabajo_autonomo", "mentoria_parcial"],
    },
    "senior": {
        "rango_anios": (4, 7),
        "caracteristicas": ["senior", "sr", "lead", "arquitecto"],
        "expectativas": ["liderazgo_tecnico", "trabajo_autonomo", "mentoria"],
    },
    "staff": {
        "rango_anios": (7, 10),
        "caracteristicas": ["staff", "principal engineer", "tech lead"],
        "expectativas": ["liderazgo_equipo", "arquitectura", "estrategia"],
    },
    "principal": {
        "rango_anios": (10, 999),
        "caracteristicas": ["principal", "distinguished", "cto", "vp"],
        "expectativas": ["estrategia_tecnica", "vision_global", "influencia"],
    },
}

REGLAS_MATCH = {
    "calculo_base": {
        "match_tecnico": "skills_coincidentes / skills_requeridas * 100",
        "match_seniority": "100 si nivel coincide, -25 por cada nivel de diferencia",
    },
    "ajustes": {
        "sin_brechas": 1.0,
        "1_brecha": 0.95,
        "2_brechas": 0.85,
        "3_brechas": 0.70,
        "4+_brechas": 0.50,
    },
    "clasificacion": {
        "excelente": (80, 100),
        "bueno": (60, 79.9),
        "regular": (40, 59.9),
        "bajo": (20, 39.9),
        "no_recomendado": (0, 19.9),
    },
}


def get_workflow(tipo: MetodoEvaluacion) -> dict:
    """Retorna el workflow según el tipo de evaluación"""
    workflows = {
        MetodoEvaluacion.ESTRUCTURADO: WORKFLOW_DEFAULT,
        MetodoEvaluacion.LANGCHAIN: WORKFLOW_LANGCHAIN,
        MetodoEvaluacion.CREW_AI: WORKFLOW_CREW,
    }
    return workflows.get(tipo, WORKFLOW_DEFAULT)


def get_reglas() -> ReglasEvaluacion:
    """Retorna las reglas de evaluación"""
    return ReglasEvaluacion()


def evaluar_coherencia(
    nivel: str, experiencia: int, skills_count: int
) -> tuple[bool, str]:
    """Evalúa coherencia entre nivel, experiencia y skills"""
    reglas = REGLAS_SENIORITY.get(nivel, {})
    rango = reglas.get("rango_anios", (0, 999))

    if experiencia < rango[0]:
        return (
            False,
            f"Experiencia ({experiencia} años) menor al mínimo para {nivel} ({rango[0]} años)",
        )
    if experiencia > rango[1]:
        return (
            False,
            f"Experiencia ({experiencia} años) mayor al máximo para {nivel} ({rango[1]} años)",
        )

    if nivel == "junior" and skills_count > 15:
        return False, "Skills avanzados detectados para nivel junior"
    if nivel in ["staff", "principal"] and skills_count < 10:
        return False, "Cantidad de skills insuficiente para nivel staff/principal"

    return True, "Coherente"
