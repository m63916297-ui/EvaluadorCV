from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import Tool
from langchain.schema import HumanMessage, SystemMessage
from typing import Optional
import json


class AgenteLangChain:
    """
    Agente Evaluador con LangChain

    Utiliza LangChain para un análisis más profundo del CV
    usando agentes y tools especializadas.
    """

    def __init__(self, api_key: str | None = None, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self.llm = None
        self._inicializar_llm()

    def _inicializar_llm(self):
        """Inicializa el modelo de LangChain"""
        try:
            self.llm = ChatOpenAI(
                model=self.model, api_key=self.api_key, temperature=0.3
            )
        except Exception:
            self.llm = None

    def analizar_cv_avanzado(self, cv_texto: str, requisitos: dict) -> dict:
        """
        Análisis avanzado del CV usando LangChain Agent
        """
        if not self.llm:
            return {"error": "LLM no disponible"}

        tools = [
            Tool(
                name="ExtraerSkills",
                func=lambda x: self._extraer_skills(x),
                description="Extrae habilidades técnicas del CV",
            ),
            Tool(
                name="EvaluarSeniority",
                func=lambda x: self._evaluar_seniority(x),
                description="Evalúa el nivel de seniority",
            ),
            Tool(
                name="DetectarBrechas",
                func=lambda x: self._detectar_brechas(x),
                description="Detecta brechas técnicas",
            ),
        ]

        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="""Eres un experto evaluador de candidatos técnicos.
Tu tarea es analizar currículums y evaluar:
1. Habilidades técnicas encontradas
2. Nivel de seniority apropiado
3. Brechas respecto a los requisitos
4. Recomendación final

Responde en formato JSON."""
                ),
                HumanMessage(
                    content=f"""
Analiza el siguiente CV:

CV:
{cv_texto[:3000]}

REQUISITOS DEL PUESTO:
- Stack requerido: {", ".join(requisitos.get("stack_tecnico", []))}
- Nivel solicitado: {requisitos.get("nivel_solicitado", "senior")}
- Experiencia mínima: {requisitos.get("experiencia_minima", 0)} años

Proporciona:
1. skills_encontradas (lista)
2. seniority_estimado (junior/semi-senior/senior/staff/principal)
3. brechas_tecnicas (lista)
4. match_porcentaje (0-100)
5. resumen (texto breve)
6. recomendacion (texto breve)
"""
                ),
            ]
        )

        try:
            response = self.llm.invoke(prompt)
            return self._parsear_respuesta(response.content)
        except Exception as e:
            return {"error": str(e)}

    def _extraer_skills(self, cv_texto: str) -> str:
        """Tool para extraer skills"""
        prompt = f"""
Extrae todas las habilidades técnicas mencionadas en este CV.
Lista solo las habilidades, una por línea:

{cv_texto[:2000]}
"""
        if self.llm:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        return ""

    def _evaluar_seniority(self, cv_texto: str) -> str:
        """Tool para evaluar seniority"""
        prompt = f"""
Evalúa el nivel de seniority basándote en el CV.
Niveles: junior (0-2 años), semi-senior (2-4), senior (4-7), staff (7-10), principal (10+)

CV:
{cv_texto[:2000]}

Responde solo con el nivel estimado.
"""
        if self.llm:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content.strip()
        return "semi-senior"

    def _detectar_brechas(self, datos: str) -> str:
        """Tool para detectar brechas"""
        if self.llm:
            response = self.llm.invoke(
                [
                    HumanMessage(
                        content=f"""
Identifica las brechas técnicas entre el CV y los requisitos.
CV y requisitos:
{datos[:2000]}

Lista las skills que faltan.
"""
                    )
                ]
            )
            return response.content
        return ""

    def _parsear_respuesta(self, respuesta: str) -> dict:
        """Parsea la respuesta JSON del agente"""
        try:
            inicio = respuesta.find("{")
            fin = respuesta.rfind("}") + 1
            if inicio != -1 and fin > inicio:
                return json.loads(respuesta[inicio:fin])
        except:
            pass
        return {"raw_response": respuesta}


class AgenteCrewAI:
    """
    Agente evaluador usando patrón Crew (múltiples agentes especializados)
    """

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key
        self.llm = None
        if api_key:
            try:
                self.llm = ChatOpenAI(api_key=api_key, temperature=0.3)
            except:
                pass

    def evaluar_con_crew(self, cv_texto: str, requisitos: dict) -> dict:
        """
        Evalúa el CV usando múltiples agentes especializados (Crew)
        """
        if not self.llm:
            return {"error": "API key requerida para Crew AI"}

        agentes = [
            ("AnalistaSkills", self._analista_skills),
            ("EvaluadorSeniority", self._evaluador_seniority),
            ("DetectorBrechas", self._detector_brechas),
        ]

        resultados = {}
        for nombre, func in agentes:
            try:
                resultados[nombre] = func(cv_texto, requisitos)
            except Exception as e:
                resultados[nombre] = {"error": str(e)}

        return self._consolidar_resultados(resultados, requisitos)

    def _analista_skills(self, cv: str, req: dict) -> dict:
        prompt = f"""Analiza el CV y extrae:
1. Skills técnicos encontrados (lista)
2. Años de experiencia mencionados
3. Certificaciones

CV: {cv[:2000]}"""
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return {"skills": response.content}

    def _evaluador_seniority(self, cv: str, req: dict) -> dict:
        prompt = f"""Evalúa el seniority apropiado para este CV.
Nivel solicitado: {req.get("nivel_solicitado", "senior")}

CV: {cv[:2000]}

Responde con nivel estimado y justificación breve."""
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return {"seniority": response.content}

    def _detector_brechas(self, cv: str, req: dict) -> dict:
        stack_req = req.get("stack_tecnico", [])
        prompt = f"""Dado el stack requerido: {", ".join(stack_req)}
¿Qué skills faltan en este CV?

CV: {cv[:2000]}"""
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return {"brechas": response.content}

    def _consolidar_resultados(self, resultados: dict, requisitos: dict) -> dict:
        """Consolida los resultados de los agentes"""
        return {
            "analisis_crew": resultados,
            "requisitos": requisitos,
            "metodo": "crew_ai",
        }
