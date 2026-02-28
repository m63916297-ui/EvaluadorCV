from typing import Optional, Any
import logging

logger = logging.getLogger(__name__)


class LLMClient:
    """Cliente LLM con soporte para OpenAI y fallback"""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self._client = None
        self._inicializar()

    def _inicializar(self):
        """Inicializa el cliente LLM"""
        if self.api_key:
            try:
                from langchain_openai import ChatOpenAI

                self._client = ChatOpenAI(
                    model=self.model, api_key=self.api_key, temperature=0.3
                )
                logger.info(f"LLM inicializado con modelo: {self.model}")
            except ImportError:
                logger.warning("langchain-openai no esta instalado, usando fallback")
                self._client = FallbackLLM()
            except Exception as e:
                logger.error(f"Error al inicializar LLM: {e}")
                self._client = FallbackLLM()
        else:
            logger.info("Sin API key, usando modo fallback")
            self._client = FallbackLLM()

    def generate(self, prompt: str) -> str:
        """Genera una respuesta"""
        try:
            if self._client is None:
                return FallbackLLM().generate(prompt)

            from langchain.schema import HumanMessage

            response = self._client.invoke([HumanMessage(content=prompt)])
            return response.content
        except Exception as e:
            logger.error(f"Error en generacion: {e}")
            return f"{{'error': '{str(e)}'}}"

    def generate_json(self, prompt: str) -> dict:
        """Genera respuesta en formato JSON"""
        prompt_json = prompt + "\n\nResponde SOLO con JSON valido, sin texto adicional."
        respuesta = self.generate(prompt_json)

        try:
            import json

            inicio = respuesta.find("{")
            fin = respuesta.rfind("}") + 1
            if inicio != -1 and fin > inicio:
                return json.loads(respuesta[inicio:fin])
        except Exception as e:
            logger.error(f"Error al parsear JSON: {e}")

        return {"raw_response": respuesta}

    @property
    def disponible(self) -> bool:
        return self._client is not None and not isinstance(self._client, FallbackLLM)


class FallbackLLM:
    """Fallback para testing sin API"""

    def generate(self, prompt: str) -> str:
        if "skills" in prompt.lower() and "extrae" in prompt.lower():
            return "Python, JavaScript, React, Docker, AWS"
        elif "seniority" in prompt.lower():
            return "senior"
        elif "brechas" in prompt.lower() or "faltan" in prompt.lower():
            return "[]"
        elif "match" in prompt.lower():
            return '{"porcentaje_match": 75.0, "clasificacion": "bueno"}'
        return '{"resultado": "simulado"}'


def create_llm_client(api_key: Optional[str] = None, model: str = "gpt-4") -> LLMClient:
    """Factory para crear cliente LLM"""
    return LLMClient(api_key=api_key, model=model)
