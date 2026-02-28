from enum import Enum
from dataclasses import dataclass
from typing import Optional


class ReglasEvaluacion:
    PESO_MATCH_TECNICO = 0.70
    PESO_MATCH_SENIORITY = 0.30
    UMBRAL_EXCELENTE = 80.0
    UMBRAL_BUENO = 60.0
    UMBRAL_REGULAR = 40.0
    PENALIZACION_BRECHA = 0.10
    MAX_BRECHAS_ACEPTABLES = 2


class JerarquiaSeniority:
    JERARQUIA = ["junior", "semi-senior", "senior", "staff", "principal"]

    @staticmethod
    def get_nivel_valido(nivel: str) -> str:
        nivel_lower = nivel.lower().strip()
        for n in JerarquiaSeniority.JERARQUIA:
            if n in nivel_lower or nivel_lower in n:
                return n
        return "semi-senior"

    @staticmethod
    def calcular_match(nivel_solicitado: str, nivel_estimado: str) -> float:
        idx_sol = (
            JerarquiaSeniority.JERARQUIA.index(nivel_solicitado)
            if nivel_solicitado in JerarquiaSeniority.JERARQUIA
            else 1
        )
        idx_est = (
            JerarquiaSeniority.JERARQUIA.index(nivel_estimado)
            if nivel_estimado in JerarquiaSeniority.JERARQUIA
            else 1
        )
        diferencia = abs(idx_sol - idx_est)

        if diferencia == 0:
            return 100.0
        elif diferencia == 1:
            return 75.0
        elif diferencia == 2:
            return 50.0
        else:
            return 25.0


SENIORITY_DEFINITIONS = {
    "junior": {
        "rango_anios": (0, 2),
        "caracteristicas": ["trainee", "junior", "entry", "practicante", "estudiante"],
        "expectativas": ["requiere_supervision", "aprendizaje_activo"],
    },
    "semi-senior": {
        "rango_anios": (2, 4),
        "caracteristicas": ["semi senior", "semi-senior", "mid-level", "intermedio"],
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
        "caracteristicas": ["principal", "distinguished", "cto", "vp engineering"],
        "expectativas": ["estrategia_tecnica", "vision_global", "influencia"],
    },
}

WORKFLOW_LANGCHAIN = {
    "agentes": [
        {
            "nombre": "AnalistaSkillsAgent",
            "descripcion": "Extrae habilidades técnicas del CV",
            "prompt_base": "Eres un analizador de CVs experto. Extrae todas las habilidades técnicas mencionadas.",
        },
        {
            "nombre": "EvaluadorSeniorityAgent",
            "descripcion": "Evalúa nivel de seniority",
            "prompt_base": "Eres un evaluador de perfiles técnicos. Determina el nivel de seniority apropiado.",
        },
        {
            "nombre": "DetectorBrechasAgent",
            "descripcion": "Identifica brechas técnicas",
            "prompt_base": "Eres un analysta de gaps. Identifica las skills que faltan.",
        },
        {
            "nombre": "CalculadorMatchAgent",
            "descripcion": "Calcula porcentaje de match",
            "prompt_base": "Eres un calculador de compatibilidad. Calcula el match entre candidato y puesto.",
        },
    ],
    "flujo": [
        "AnalistaSkills",
        "EvaluadorSeniority",
        "DetectorBrechas",
        "CalculadorMatch",
    ],
}


def get_clasificacion(match: float) -> str:
    if match >= ReglasEvaluacion.UMBRAL_EXCELENTE:
        return "excelente"
    elif match >= ReglasEvaluacion.UMBRAL_BUENO:
        return "bueno"
    elif match >= ReglasEvaluacion.UMBRAL_REGULAR:
        return "regular"
    else:
        return "no_recomendado"
