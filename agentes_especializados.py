from typing import Dict, Any
from agente_base import AgenteBase, PROMPTS
import re
import logging

logger = logging.getLogger(__name__)

CATEGORIAS_SKILLS = {
    "lenguajes": [
        "python",
        "javascript",
        "typescript",
        "java",
        "c#",
        "go",
        "rust",
        "ruby",
        "php",
        "swift",
        "kotlin",
        "scala",
        "r",
    ],
    "frameworks": [
        "react",
        "vue",
        "angular",
        "django",
        "flask",
        "fastapi",
        "express",
        "spring",
        "laravel",
        "next.js",
        "nuxt",
    ],
    "ml_ai": [
        "tensorflow",
        "pytorch",
        "keras",
        "scikit-learn",
        "langchain",
        "langchain-architecture",
        "langchain-orchestration",
        "llamaindex",
        "openai",
        "gpt",
        "transformers",
        "bert",
        "rag",
        "llm",
    ],
    "databases": [
        "postgresql",
        "mysql",
        "mongodb",
        "redis",
        "elasticsearch",
        "faiss",
        "pinecone",
        "weaviate",
        "chroma",
    ],
    "cloud": ["aws", "azure", "gcp", "docker", "kubernetes", "terraform", "jenkins"],
    "metodologias": ["agile", "scrum", "devops", "ci/cd", "tdd"],
}


class AgenteAnalistaSkills(AgenteBase):
    """Agente especializado en extraer skills del CV"""

    def __init__(self, llm_client):
        super().__init__("AnalistaSkills", llm_client)
        self.prompt = PROMPTS["analista_skills"]

    def ejecutar(self, input_data: dict) -> dict:
        cv_texto = input_data.get("cv_texto", "")

        if self.llm.disponible:
            prompt_completo = self.prompt.user_template.format(cv_texto=cv_texto)
            respuesta = self.llm.generate_json(prompt_completo)
            return self._parsear_respuesta(respuesta, cv_texto)

        return self._extraer_local(cv_texto)

    def _parsear_respuesta(self, respuesta: dict, cv_texto: str) -> dict:
        return {
            "skills_tecnicas": respuesta.get("skills_tecnicas", []),
            "skills_blandas": respuesta.get("skills_blandas", []),
            "experiencia_anios": respuesta.get(
                "experiencia_anios", self._extraer_experiencia(cv_texto)
            ),
            "nivel_autodetectado": respuesta.get("nivel_autodetectado", "senior"),
        }

    def _extraer_local(self, cv_texto: str) -> dict:
        cv_lower = cv_texto.lower()
        skills_encontradas = []

        for categoria, skills in CATEGORIAS_SKILLS.items():
            for skill in skills:
                if skill in cv_lower:
                    skills_encontradas.append(skill)

        experiencia = self._extraer_experiencia(cv_texto)

        return {
            "skills_tecnicas": list(set(skills_encontradas)),
            "skills_blandas": [],
            "experiencia_anios": experiencia,
            "nivel_autodetectado": "senior"
            if experiencia >= 4
            else "junior"
            if experiencia <= 2
            else "semi-senior",
        }

    def _extraer_experiencia(self, texto: str) -> int:
        patrones = [
            r"(\d+)\+?\s*años?\s+de\s+experiencia",
            r"(\d+)\+?\s*years?\s+experience",
            r"experiencia:\s*(\d+)\s*años?",
        ]
        for patron in patrones:
            match = re.search(patron, texto, re.IGNORECASE)
            if match:
                return int(match.group(1))
        return 0


class AgenteEvaluadorSeniority(AgenteBase):
    """Agente especializado en evaluar nivel de seniority"""

    def __init__(self, llm_client):
        super().__init__("EvaluadorSeniority", llm_client)
        self.prompt = PROMPTS["evaluador_seniority"]

    def ejecutar(self, input_data: dict) -> dict:
        cv_texto = input_data.get("cv_texto", "")
        nivel_solicitado = input_data.get("nivel_solicitado", "senior")
        exp_minima = input_data.get("experiencia_minima", 0)

        if self.llm.disponible:
            prompt_completo = self.prompt.user_template.format(
                cv_texto=cv_texto,
                nivel_solicitado=nivel_solicitado,
                exp_minima=exp_minima,
            )
            return self.llm.generate_json(prompt_completo)

        return self._evaluar_local(cv_texto, nivel_solicitado, exp_minima)

    def _evaluar_local(self, cv: str, nivel_sol: str, exp_min: int) -> dict:
        experiencia = self._extraer_experiencia(cv)

        if experiencia <= 2:
            nivel = "junior"
        elif experiencia <= 4:
            nivel = "semi-senior"
        elif experiencia <= 7:
            nivel = "senior"
        elif experiencia <= 10:
            nivel = "staff"
        else:
            nivel = "principal"

        coherente = (
            abs(
                ["junior", "semi-senior", "senior", "staff", "principal"].index(nivel)
                - ["junior", "semi-senior", "senior", "staff", "principal"].index(
                    nivel_sol
                )
            )
            <= 1
        )

        return {
            "seniority_estimado": nivel,
            "experiencia_detectada": experiencia,
            "fundamento": f"Basado en {experiencia} anos de experiencia",
            "coherente": coherente,
            "indicadores_encontrados": self._buscar_indicadores(cv),
        }

    def _extraer_experiencia(self, texto: str) -> int:
        import re

        patrones = [r"(\d+)\+?\s*años?", r"(\d+)\+?\s*years?"]
        for patron in patrones:
            match = re.search(patron, texto, re.IGNORECASE)
            if match:
                return int(match.group(1))
        return 0

    def _buscar_indicadores(self, cv: str) -> list:
        indicadores = []
        cv_lower = cv.lower()

        if "senior" in cv_lower or "sr" in cv_lower:
            indicadores.append("senior")
        if "lead" in cv_lower or "arquitecto" in cv_lower:
            indicadores.append("lead")
        if "principal" in cv_lower or "staff" in cv_lower:
            indicadores.append("staff")

        return indicadores


class AgenteDetectorBrechas(AgenteBase):
    """Agente especializado en detectar brechas tecnicas"""

    def __init__(self, llm_client):
        super().__init__("DetectorBrechas", llm_client)
        self.prompt = PROMPTS["detector_brechas"]

    def ejecutar(self, input_data: dict) -> dict:
        skills_encontradas = input_data.get("skills_encontradas", [])
        stack_requerido = input_data.get("stack_requerido", [])

        if self.llm.disponible:
            prompt_completo = self.prompt.user_template.format(
                cv_texto=input_data.get("cv_texto", "")[:2000],
                stack_requerido=", ".join(stack_requerido),
            )
            return self.llm.generate_json(prompt_completo)

        return self._detectar_local(skills_encontradas, stack_requerido)

    def _detectar_local(self, skills_cv: list, requerido: list) -> dict:
        skills_cv_lower = [s.lower() for s in skills_cv]

        brechas_criticas = []
        skills_coincidentes = []

        for req in requerido:
            encontrado = False
            req_lower = req.lower()
            for skill in skills_cv_lower:
                if req_lower in skill or skill in req_lower:
                    skills_coincidentes.append(req)
                    encontrado = True
                    break
            if not encontrado:
                brechas_criticas.append(req)

        return {
            "brechas_criticas": brechas_criticas,
            "brechas_deseables": [],
            "skills_coincidentes": skills_coincidentes,
            "evaluacion_global": f"{len(skills_coincidentes)} de {len(requerido)} skills cubiertas",
        }


class AgenteCalculadorMatch(AgenteBase):
    """Agente especializado en calcular porcentaje de match"""

    def __init__(self, llm_client):
        super().__init__("CalculadorMatch", llm_client)
        self.prompt = PROMPTS["calculador_match"]

    def ejecutar(self, input_data: dict) -> dict:
        skills_encontradas = input_data.get("skills_encontradas", [])
        stack_requerido = input_data.get("stack_requerido", [])
        seniority_estimado = input_data.get("seniority_estimado", "semi-senior")
        nivel_solicitado = input_data.get("nivel_solicitado", "senior")
        brechas = input_data.get("brechas_criticas", [])

        if self.llm.disponible:
            prompt_completo = self.prompt.user_template.format(
                skills_encontradas=", ".join(skills_encontradas),
                stack_requerido=", ".join(stack_requerido),
                seniority_estimado=seniority_estimado,
                nivel_solicitado=nivel_solicitado,
                brechas=", ".join(brechas),
            )
            return self.llm.generate_json(prompt_completo)

        return self._calcular_local(
            skills_encontradas,
            stack_requerido,
            seniority_estimado,
            nivel_solicitado,
            brechas,
        )

    def _calcular_local(
        self,
        skills_cv: list,
        requerido: list,
        nivel_est: str,
        nivel_sol: str,
        brechas: list,
    ) -> dict:

        match_tecnico = (len(skills_cv) / len(requerido) * 100) if requerido else 100
        match_tecnico = min(match_tecnico, 100)

        jerarquia = {
            "junior": 1,
            "semi-senior": 2,
            "senior": 3,
            "staff": 4,
            "principal": 5,
        }
        diff = abs(jerarquia.get(nivel_est, 2) - jerarquia.get(nivel_sol, 3))
        match_seniority = 100 - (diff * 25)

        penalizacion = min(len(brechas) * 10, 50)
        match_total = (match_tecnico * 0.7 + match_seniority * 0.3) - penalizacion
        match_total = max(0, min(match_total, 100))

        if match_total >= 80:
            clasificacion = "excelente"
        elif match_total >= 60:
            clasificacion = "bueno"
        elif match_total >= 40:
            clasificacion = "regular"
        else:
            clasificacion = "no_recomendado"

        return {
            "porcentaje_match": round(match_total, 1),
            "match_tecnico": round(match_tecnico, 1),
            "match_seniority": round(match_seniority, 1),
            "clasificacion": clasificacion,
            "resumen": f"Match tecnico: {match_tecnico:.0f}%, Match seniority: {match_seniority:.0f}%",
        }
