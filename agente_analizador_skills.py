from typing import List


class AgenteAnalizadorSkills:
    """Analiza y extrae skills técnicas y blandas del CV"""

    CATEGORIAS_SKILLS = {
        "lenguajes_programacion": [
            "python",
            "javascript",
            "typescript",
            "java",
            "c#",
            "c++",
            "go",
            "rust",
            "ruby",
            "php",
            "swift",
            "kotlin",
            "scala",
            "r",
            "matlab",
        ],
        "frameworks_frontend": [
            "react",
            "vue",
            "angular",
            "svelte",
            "next.js",
            "nuxt",
            "gatsby",
            "bootstrap",
            "tailwind",
            "material-ui",
            "redux",
            "zustand",
        ],
        "frameworks_backend": [
            "django",
            "flask",
            "fastapi",
            "express",
            "spring",
            "laravel",
            "rails",
            ".net",
            "nestjs",
            "",
            "hapifastify",
        ],
        "bases_datos": [
            "postgresql",
            "mysql",
            "mongodb",
            "redis",
            "elasticsearch",
            "oracle",
            "sql server",
            "firebase",
            "supabase",
            "dynamodb",
        ],
        "cloud_devops": [
            "aws",
            "azure",
            "gcp",
            "docker",
            "kubernetes",
            "terraform",
            "ansible",
            "jenkins",
            "github actions",
            "gitlab ci",
            "nginx",
        ],
        "metodologias": ["agile", "scrum", "kanban", "devops", "ci/cd", "tdd", "bdd"],
        "habilidades_blandas": [
            "liderazgo",
            "comunicacion",
            "trabajo en equipo",
            "resolucion de problemas",
            "gestion de proyectos",
            "mentoria",
            "presentaciones",
        ],
    }

    def __init__(self, llm_client):
        self.llm = llm_client

    def analizar(self, cv_texto: str) -> dict:
        """Analiza el CV y extrae todas las skills encontradas"""
        cv_lower = cv_texto.lower()

        skills_encontradas = {
            "lenguajes_programacion": [],
            "frameworks_frontend": [],
            "frameworks_backend": [],
            "bases_datos": [],
            "cloud_devops": [],
            "metodologias": [],
            "habilidades_blandas": [],
        }

        for categoria, skills in self.CATEGORIAS_SKILLS.items():
            for skill in skills:
                if skill in cv_lower:
                    skills_encontradas[categoria].append(skill)

        experiencia = self._extraer_experiencia(cv_texto)

        return {
            "skills": skills_encontradas,
            "experiencia_anios": experiencia,
            "skills_principales": self._extraer_skills_principales(cv_texto),
        }

    def _extraer_experiencia(self, cv_texto: str) -> int:
        """Extrae años de experiencia del CV"""
        import re

        patrones = [
            r"(\d+)\+?\s*años?\s+de\s+experiencia",
            r"(\d+)\+?\s*years?\s+experience",
            r"experiencia:\s*(\d+)\s*años?",
        ]
        for patron in patrones:
            match = re.search(patron, cv_texto, re.IGNORECASE)
            if match:
                return int(match.group(1))
        return 0

    def _extraer_skills_principales(self, cv_texto: str) -> List[str]:
        """Usa LLM para identificar skills principales mencionadas"""
        prompt = f"""
Analiza el siguiente CV y lista las 10 habilidades técnicas más importantes 
que posee el candidato, ordenadas por relevancia:

{cv_texto[:2000]}

Responde solo con una lista de habilidades, una por línea.
"""
        resultado = self.llm.generate(prompt)
        return [s.strip() for s in resultado.strip().split("\n") if s.strip()]
