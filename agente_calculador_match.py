class AgenteCalculadorMatch:
    """Calcula el porcentaje de match entre el CV y los requisitos del puesto"""

    def __init__(self, llm_client):
        self.llm = llm_client

    def calcular(self, skills_cv: dict, requisitos: dict, brechas: dict) -> dict:
        """Calcula el porcentaje de match"""

        stack_requerido = requisitos.get("stack_tecnico", [])
        nivel_solicitado = requisitos.get("nivel_solicitado", "semi-senior")

        match_tecnico = self._calcular_match_tecnico(
            stack_requerido, brechas.get("skills_coincidentes", [])
        )

        match_seniority = self._calcular_match_seniority(
            nivel_solicitado, brechas.get("seniority_estimado", "junior")
        )

        peso_tecnico = 0.7
        peso_seniority = 0.3

        match_total = (match_tecnico * peso_tecnico) + (
            match_seniority * peso_seniority
        )

        ajuste_por_brechas = self._ajuste_por_brechas(brechas, match_total)

        return {
            "porcentaje_match": round(ajuste_por_brechas, 1),
            "match_tecnico": round(match_tecnico, 1),
            "match_seniority": round(match_seniority, 1),
            "nivel_solicitado": nivel_solicitado,
            "nivel_estimado": brechas.get("seniority_estimado", "junior"),
            "clasificacion": self._clasificar_candidato(ajuste_por_brechas),
            "resumen": self._generar_resumen(
                match_total, match_tecnico, match_seniority, brechas
            ),
        }

    def _calcular_match_tecnico(self, requerido: list, coincidentes: list) -> float:
        """Calcula el match técnico"""
        if not requerido:
            return 100.0

        return (len(coincidentes) / len(requerido)) * 100

    def _calcular_match_seniority(self, solicitado: str, estimado: str) -> float:
        """Calcula el match de seniority"""
        jerarquia = {
            "junior": 1,
            "semi-senior": 2,
            "senior": 3,
            "staff": 4,
            "principal": 5,
        }

        nivel_sol = jerarquia.get(solicitado.lower(), 2)
        nivel_est = jerarquia.get(estimado.lower(), 1)

        diferencia = abs(nivel_sol - nivel_est)

        if diferencia == 0:
            return 100.0
        elif diferencia == 1:
            return 75.0
        elif diferencia == 2:
            return 50.0
        else:
            return 25.0

    def _ajuste_por_brechas(self, brechas: dict, match_base: float) -> float:
        """Ajusta el match basado en las brechas"""
        num_brechas = len(brechas.get("brechas_tecnicas", []))

        if num_brechas == 0:
            return match_base
        elif num_brechas == 1:
            return match_base * 0.95
        elif num_brechas == 2:
            return match_base * 0.85
        elif num_brechas == 3:
            return match_base * 0.70
        else:
            return match_base * 0.50

    def _clasificar_candidato(self, match: float) -> str:
        """Clasifica al candidato basado en el match"""
        if match >= 80:
            return "excelente"
        elif match >= 60:
            return "bueno"
        elif match >= 40:
            return "regular"
        elif match >= 20:
            return "bajo"
        else:
            return "no_recomendado"

    def _generar_resumen(
        self,
        match_total: float,
        match_tecnico: float,
        match_seniority: float,
        brechas: dict,
    ) -> str:
        """Genera un resumen de la evaluación"""
        clasificacion = self._clasificar_candidato(match_total)

        resumen = f"Match total: {match_total:.1f}% "
        resumen += (
            f"(Técnico: {match_tecnico:.1f}%, Seniority: {match_seniority:.1f}%). "
        )

        if brechas.get("brechas_tecnicas"):
            resumen += f"Brechas: {', '.join(brechas['brechas_tecnicas'][:3])}. "

        if clasificacion == "excelente":
            resumen += "Candidato muy recomendado para el puesto."
        elif clasificacion == "bueno":
            resumen += "Candidato recomendado, considerar brechas menores."
        elif clasificacion == "regular":
            resumen += "Candidato parcialmente adecuado, requiere evaluación adicional."
        else:
            resumen += "No se recomienda para el puesto solicitado."

        return resumen
