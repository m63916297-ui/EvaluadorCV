from typing import List


class AgenteDetectorBrechas:
    """Detecta las brechas técnicas entre el CV y los requisitos del puesto"""

    def __init__(self, llm_client):
        self.llm = llm_client

    def detectar(self, skills_cv: dict, requisitos: dict) -> dict:
        """Detecta brechas entre skills del CV y requisitos"""

        skills_requeridas = requisitos.get("stack_tecnico", [])
        skills_blandas_requeridas = requisitos.get("habilidades_blandas", [])

        todas_skills_cv = self._flatten_skills(skills_cv)

        brechas_duras = self._detectar_brechas_duras(skills_requeridas, todas_skills_cv)
        brechas_blandas = self._detectar_brechas_blandas(
            skills_blandas_requeridas, skills_cv.get("habilidades_blandas", [])
        )

        skills_match = self._identificar_skills_match(
            skills_requeridas, todas_skills_cv
        )

        criticidad = self._evaluar_criticidad(brechas_duras, skills_requeridas)

        return {
            "brechas_tecnicas": brechas_duras,
            "brechas_blandas": brechas_blandas,
            "skills_coincidentes": skills_match,
            "criticidad": criticidad,
            "puede_ser_candidato": len(brechas_duras) <= 2,
            "recomendacion": self._generar_recomendacion(brechas_duras, criticidad),
        }

    def _flatten_skills(self, skills: dict) -> List[str]:
        """Convierte el diccionario de skills en una lista plana"""
        todas = []
        for categoria, lista in skills.items():
            todas.extend([s.lower() for s in lista])
        return todas

    def _detectar_brechas_duras(
        self, requeridas: List[str], cv_skills: List[str]
    ) -> List[str]:
        """Detecta skills técnicas que faltan"""
        cv_lower = [s.lower() for s in cv_skills]
        brechas = []

        for req in requeridas:
            encontrado = False
            req_lower = req.lower()
            for skill in cv_lower:
                if req_lower in skill or skill in req_lower:
                    encontrado = True
                    break
            if not encontrado:
                brechas.append(req)

        return brechas

    def _detectar_brechas_blandas(
        self, requeridas: List[str], blandas_cv: List[str]
    ) -> List[str]:
        """Detecta habilidades blandas que faltan"""
        cv_lower = [s.lower() for s in blandas_cv]
        brechas = []

        for req in requeridas:
            encontrado = False
            req_lower = req.lower()
            for habilidad in cv_lower:
                if req_lower in habilidad or habilidad in req_lower:
                    encontrado = True
                    break
            if not encontrado:
                brechas.append(req)

        return brechas

    def _identificar_skills_match(
        self, requeridas: List[str], cv_skills: List[str]
    ) -> List[str]:
        """Identifica las skills que coinciden"""
        cv_lower = [s.lower() for s in cv_skills]
        match = []

        for req in requeridas:
            req_lower = req.lower()
            for skill in cv_lower:
                if req_lower in skill or skill in req_lower:
                    match.append(req)
                    break

        return match

    def _evaluar_criticidad(
        self, brechas: List[str], todas_requeridas: List[str]
    ) -> str:
        """Evalúa la criticidad de las brechas"""
        if not brechas:
            return "baja"

        porcentaje_falta = (
            len(brechas) / len(todas_requeridas) if todas_requeridas else 0
        )

        if porcentaje_falta > 0.5:
            return "alta"
        elif porcentaje_falta > 0.25:
            return "media"
        else:
            return "baja"

    def _generar_recomendacion(self, brechas: List[str], criticidad: str) -> str:
        """Genera una recomendación basada en las brechas"""
        if not brechas:
            return "El candidato cumple con todos los requisitos técnicos."

        if criticidad == "alta":
            return f"Brechas significativas: {', '.join(brechas[:3])}. Se recomienda no proceder."
        elif criticidad == "media":
            return f"Brechas moderadas detectadas: {', '.join(brechas[:2])}. Considerar para posiciones junior."
        else:
            return f"Brechas menores: {', '.join(brechas)}. Candidate viable con capacitación."
