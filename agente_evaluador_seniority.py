class AgenteEvaluadorSeniority:
    """Evalúa el nivel de seniority del candidato basado en su CV"""

    NIVELES = {
        "junior": {
            "descripcion": "0-2 años de experiencia, requiere supervisión",
            "indicadores": ["junior", "entry", "trainee", "practicante", "estudiante"],
            "max_experiencia": 2,
        },
        "semi-senior": {
            "descripcion": "2-4 años de experiencia, trabajo autónomo",
            "indicadores": ["semi senior", "semi-senior", "mid-level", "intermedio"],
            "min_experiencia": 2,
            "max_experiencia": 4,
        },
        "senior": {
            "descripcion": "4-7 años de experiencia, liderazgo técnico",
            "indicadores": ["senior", "sr", "lead", "arquitecto", "principal"],
            "min_experiencia": 4,
            "max_experiencia": 7,
        },
        "staff": {
            "descripcion": "7-10 años, liderazgo de equipos técnicos",
            "indicadores": ["staff", "principal engineer", "tech lead"],
            "min_experiencia": 7,
            "max_experiencia": 10,
        },
        "principal": {
            "descripcion": "10+ años, estrategia técnica全局",
            "indicadores": [
                "principal",
                "distinguished",
                "fellow",
                "cto",
                "vp engineering",
            ],
            "min_experiencia": 10,
        },
    }

    def __init__(self, llm_client):
        self.llm = llm_client

    def evaluar(self, cv_texto: str, experiencia_anios: int, skills: dict) -> dict:
        """Evalúa el nivel de seniority del candidato"""

        nivel_basico = self._evaluacion_por_experiencia(experiencia_anios)
        nivel_por_roles = self._evaluacion_por_roles(cv_texto)
        nivel_por_skills = self._evaluacion_por_complexidad(skills)

        nivel_final = self._consolidar_evaluacion(
            nivel_basico, nivel_por_roles, nivel_por_skills
        )

        coherencia = self._verificar_coherencia(nivel_final, experiencia_anios, skills)

        return {
            "seniority_estimado": nivel_final,
            "experiencia_detectada": experiencia_anios,
            "fundamento": self._generar_fundamento(
                nivel_final, experiencia_anios, skills
            ),
            "coherente": coherencia,
            "nivel_similar": nivel_por_roles == nivel_basico,
        }

    def _evaluacion_por_experiencia(self, anios: int) -> str:
        """Evalúa basado en años de experiencia"""
        if anios <= 2:
            return "junior"
        elif anios <= 4:
            return "semi-senior"
        elif anios <= 7:
            return "senior"
        elif anios <= 10:
            return "staff"
        else:
            return "principal"

    def _evaluacion_por_roles(self, cv_texto: str) -> str:
        """Evalúa basado en títulos/roles mencionados"""
        cv_lower = cv_texto.lower()
        niveles_encontrados = []

        for nivel, config in self.NIVELES.items():
            for indicador in config["indicadores"]:
                if indicador in cv_lower:
                    niveles_encontrados.append(nivel)
                    break

        if not niveles_encontrados:
            return "junior"

        jerarquia = ["junior", "semi-senior", "senior", "staff", "principal"]
        return max(niveles_encontrados, key=lambda x: jerarquia.index(x))

    def _evaluacion_por_complexidad(self, skills: dict) -> str:
        """Evalúa basado en la complejidad del stack técnico"""
        total_skills = sum(len(v) for v in skills.values())

        frameworks_count = len(skills.get("frameworks_frontend", [])) + len(
            skills.get("frameworks_backend", [])
        )
        cloud_count = len(skills.get("cloud_devops", []))

        if total_skills >= 15 and cloud_count >= 3:
            return "senior"
        elif total_skills >= 10 and frameworks_count >= 2:
            return "semi-senior"
        elif total_skills >= 5:
            return "junior"
        else:
            return "junior"

    def _consolidar_evaluacion(self, exp: str, roles: str, skills: str) -> str:
        """Consolida las tres evaluaciones en una"""
        jerarquia = {
            "junior": 1,
            "semi-senior": 2,
            "senior": 3,
            "staff": 4,
            "principal": 5,
        }

        valores = [jerarquia[exp], jerarquia[roles], jerarquia[skills]]
        promedio = sum(valores) / len(valores)

        for nivel, valor in jerarquia.items():
            if valor >= promedio:
                return nivel
        return "junior"

    def _verificar_coherencia(self, nivel: str, experiencia: int, skills: dict) -> bool:
        """Verifica si el nivel estimado es coherente"""
        if nivel == "junior" and experiencia > 3:
            return False
        if nivel in ["staff", "principal"] and experiencia < 5:
            return False
        return True

    def _generar_fundamento(self, nivel: str, experiencia: int, skills: dict) -> str:
        """Genera una explicación del nivel asignado"""
        fundamentos = {
            "junior": f"Candidato junior con {experiencia} años de experiencia. ",
            "semi-senior": f"Candidato semi-senior con {experiencia} años de experiencia. ",
            "senior": f"Candidato senior con {experiencia} años de experiencia. ",
            "staff": f"Candidato staff con {experiencia} años de experiencia. ",
            "principal": f"Candidato de nivel principal con {experiencia} años de experiencia. ",
        }

        total_skills = sum(len(v) for v in skills.values())
        fundamentos[nivel] += (
            f"Manejo de {total_skills} habilidades técnicas detectadas."
        )

        return fundamentos[nivel]
