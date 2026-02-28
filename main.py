"""
Evaluador de CV - Sistema Multiagente con LangChain

Funcion principal para evaluar candidatos tecnicos.
"""

from typing import Optional
import logging
import json

from modelos import ResultadoEvaluacion, ResultadoCompleto, RequisitosPuesto
from agente_coordinador import (
    AgenteCoordinador,
    crear_coordinador,
    ConfiguracionEvaluacion,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def evaluar_cv(
    cv_texto: str,
    stack_requerido: list[str],
    nivel_solicitado: str,
    experiencia_minima: int = 0,
    habilidades_blandas: list[str] | None = None,
    api_key: str | None = None,
    modelo: str = "gpt-4",
    devolver_trazabilidad: bool = False,
) -> ResultadoEvaluacion | ResultadoCompleto:
    """
    Evalua un CV contra los requisitos del puesto.

    Args:
        cv_texto: Contenido del CV en texto plano
        stack_requerido: Lista de tecnologias/skills requeridas
        nivel_solicitado: Nivel buscado (junior/semi-senior/senior/staff/principal)
        experiencia_minima: Anos de experiencia minimos requeridos
        habilidades_blandas: Habilidades blandas requeridas
        api_key: Clave API de OpenAI (opcional)
        modelo: Modelo a usar (default: gpt-4)
        devolver_trazabilidad: Si True, devuelve ResultadoCompleto con trazabilidad

    Returns:
        ResultadoEvaluacion: Resultado basico de la evaluacion
        ResultadoCompleto: Resultado con trazabilidad si devolver_trazabilidad=True

    Example:
        >>> resultado = evaluar_cv(
        ...     cv_texto="...",
        ...     stack_requerido=["Python", "React", "AWS"],
        ...     nivel_solicitado="senior",
        ...     experiencia_minima=3
        ... )
        >>> print(resultado.porcentaje_match)
        85.5
    """
    logger.info(f"Iniciando evaluacion para nivel: {nivel_solicitado}")

    config = ConfiguracionEvaluacion(
        api_key=api_key, modelo=modelo, usar_langchain=api_key is not None
    )

    coordinador = AgenteCoordinador(config)

    resultado_completo = coordinador.evaluar(
        cv_texto=cv_texto,
        stack_requerido=stack_requerido,
        nivel_solicitado=nivel_solicitado,
        experiencia_minima=experiencia_minima,
        habilidades_blandas=habilidades_blandas or [],
    )

    if devolver_trazabilidad:
        return resultado_completo

    return resultado_completo.resultado


def evaluar_cv_desde_dict(datos: dict) -> dict:
    """
    Evalua un CV desde un diccionario.

    Args:
        datos: Diccionario con:
            - cv: texto del CV
            - stack_requerido: lista de skills
            - nivel_solicitado: nivel requerido
            - experiencia_minima: (opcional) anos minimos
            - api_key: (opcional) API key

    Returns:
        Diccionario con el resultado en JSON
    """
    resultado = evaluar_cv(
        cv_texto=datos["cv"],
        stack_requerido=datos["stack_requerido"],
        nivel_solicitado=datos["nivel_solicitado"],
        experiencia_minima=datos.get("experiencia_minima", 0),
        habilidades_blandas=datos.get("habilidades_blandas", []),
        api_key=datos.get("api_key"),
    )

    return {
        "porcentaje_match": resultado.porcentaje_match,
        "seniority_estimado": resultado.seniority_estimado,
        "brechas_tecnicas": resultado.brechas_tecnicas,
        "skills_encontradas": resultado.skills_encontradas,
        "skills_faltantes": resultado.skills_faltantes,
        "nivel_coherente": resultado.nivel_coherente,
        "resumen": resultado.resumen_evaluacion,
    }


def ejemplo_ejecucion():
    """Ejemplo de uso del sistema"""

    CV_EJEMPLO = """
    MARIA GARCIA - INGENIERA DE SOFTWARE AI
    
    RESUMEN:
    Ingeniera de software con 5 anos de experiencia en desarrollo de aplicaciones
    con capacidades de Inteligencia Artificial. Especializacion en arquitecturas
    RAG y despliegue de modelos LLM.
    
    EXPERIENCIA: 5 anos
    
    HABILIDADES TECNICAS:
    - Python, TypeScript, Go
    - LangChain, LangChain-Architecture, LangChain-Orchestration
    - FastAPI, Django, React
    - OpenAI API, GPT-4, Claude
    - Pinecone, Weaviate, Chroma
    - Docker, Kubernetes, AWS
    - PostgreSQL, MongoDB, Redis
    
    EXPERIENCIA LABORAL:
    - Senior AI Engineer en TechCorp (2021-presente)
    - Full Stack Developer en StartupXYZ (2018-2021)
    """

    STACK_REQUERIDO = [
        "Python",
        "LangChain",
        "LangChain-Architecture",
        "LangChain-Orchestration",
        "OpenAI",
        "FastAPI",
        "Docker",
        "AWS",
        "PostgreSQL",
    ]

    print("=" * 60)
    print("EVALUADOR DE HOJAS DE VIDA - EJEMPLO")
    print("=" * 60)
    print()

    print("CV del candidato:")
    print(CV_EJEMPLO[:200] + "...")
    print()
    print("Stack requerido:", STACK_REQUERIDO)
    print()

    resultado = evaluar_cv(
        cv_texto=CV_EJEMPLO,
        stack_requerido=STACK_REQUERIDO,
        nivel_solicitado="senior",
        experiencia_minima=3,
    )

    print("RESULTADO:")
    print("-" * 40)
    print(f"Match: {resultado.porcentaje_match}%")
    print(f"Seniority: {resultado.seniority_estimado}")
    print(f"Coherente: {'Si' if resultado.nivel_coherente else 'No'}")
    print()
    print("Skills encontradas:", resultado.skills_encontradas)
    print()
    print("Brechas:", resultado.brechas_tecnicas)
    print()
    print("Resumen:", resultado.resumen_evaluacion)
    print("=" * 60)


if __name__ == "__main__":
    ejemplo_ejecucion()
