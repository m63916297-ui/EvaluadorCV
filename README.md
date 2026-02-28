# Evaluador de CV - Sistema Multiagente con LangChain

Sistema de evaluación de currículums vitae usando arquitectura multiagente con LangChain.

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                    AgenteCoordinador                            │
│               (Orquestación del flujo)                        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
      ┌────────────────────┼────────────────────┐
      │                    │                    │
      v                    v                    v
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Analista  │    │  Evaluador  │    │  Detector   │
│   Skills    │───▶│  Seniority  │───▶│   Brechas   │
└─────────────┘    └─────────────┘    └──────┬──────┘
                                             │
                                             v
                                     ┌─────────────┐
                                     │  Calculador │
                                     │    Match    │
                                     └─────────────┘
```

## Estructura del Proyecto

```
evaluadorCV/
├── modelos.py                 # Tipos de datos y resultados
├── reglas.py                  # Reglas de evaluación
├── templates.py              # Templates de CV para 7 profesionales
├── llm_client.py            # Cliente LLM con LangChain
├── agente_base.py           # Clase base y prompts estructurados
├── agentes_especializados.py # 4 agentes especializados
├── agente_coordinador.py    # Orquestador del flujo
├── main.py                  # API principal
├── streamlit_app.py         # Interfaz Streamlit
├── requirements.txt         # Dependencias
├── .streamlit/config.toml  # Configuración
└── README.md               # Documentación
```

## Instalación

```bash
cd evaluadorCV
pip install -r requirements.txt
```

## Uso Programático

```python
from main import evaluar_cv

# Ejemplo básico
resultado = evaluar_cv(
    cv_texto="""
    JUAN PEREZ - Ingeniero de Software
    
    5 años de experiencia en Python, JavaScript, React, Docker, AWS.
    """,
    stack_requerido=["Python", "React", "AWS", "Docker"],
    nivel_solicitado="senior",
    experiencia_minima=3
)

print(f"Match: {resultado.porcentaje_match}%")
print(f"Seniority: {resultado.seniority_estimado}")
print(f"Brechas: {resultado.brechas_tecnicas}")
```

## Tipos de Profesionales Soportados

1. **Ingeniero ML** - Machine Learning Engineer
2. **Data Scientist** - Científico de Datos
3. **Software Engineer AI** - Incluyendo LangChain-Architecture y LangChain-Orchestration
4. **Fullstack Developer** - Desarrollador Full Stack
5. **Experto Ciberseguridad** - Security Expert
6. **Frontend Developer** - Desarrollador Frontend
7. **Backend Developer** - Desarrollador Backend

## Skills Incluidos

### LangChain
- **LangChain-Architecture**: Diseño de arquitecturas con LangChain
- **LangChain-Orchestration**: Orquestación de agentes y chains

### Otros Skills
- Python, JavaScript, TypeScript, Go, Java
- React, Vue, Angular, Django, FastAPI
- TensorFlow, PyTorch, Scikit-learn
- PostgreSQL, MongoDB, Redis, Pinecone, Weaviate
- AWS, Azure, GCP, Docker, Kubernetes

## Reglas de Evaluación

### Seniority
| Nivel    | Años Exp. | Características                    |
|----------|-----------|-----------------------------------|
| Junior   | 0-2       | trainee, entry, practicante       |
| Semi-sr  | 2-4       | trabajo autónomo                  |
| Senior   | 4-7       | liderazgo técnico                 |
| Staff    | 7-10      | liderazgo de equipos              |
| Principal| 10+       | estrategia técnica                |

### Cálculo de Match
- **Match Técnico**: 70% del peso
  - `% skills que coinciden`
- **Match Seniority**: 30% del peso
  - 100% si coincide, -25% por cada nivel de diferencia
- **Penalización por brechas**: -10% por cada skill faltante

### Clasificación
| Score   | Clasificación |
|---------|---------------|
| 80-100% | Excelente     |
| 60-79%  | Bueno         |
| 40-59%  | Regular       |
| 0-39%   | No recomendado|

## Ejemplo de Input/Output

### Input
```python
cv_texto = """
MARIA GARCIA - Ingeniera de Software AI

5 años de experiencia en desarrollo Python, LangChain, FastAPI.
Skills: Python, LangChain, LangChain-Architecture, OpenAI, Docker, AWS
"""

stack_requerido = ["Python", "LangChain", "FastAPI", "Docker", "AWS"]
nivel_solicitado = "senior"
```

### Output
```json
{
  "porcentaje_match": 85.5,
  "seniority_estimado": "senior",
  "brechas_tecnicas": [],
  "skills_encontradas": ["Python", "LangChain", "FastAPI", "Docker", "AWS"],
  "skills_faltantes": [],
  "nivel_coherente": true,
  "resumen_evaluacion": "Match técnico: 100%, Match seniority: 75%"
}
```

## Trazabilidad

El sistema registra cada paso de la ejecución:

```python
resultado = evaluar_cv(
    cv_texto=...,
    stack_requerido=...,
    nivel_solicitado=...,
    devolver_trazabilidad=True  # Returns ResultadoCompleto
)

# Acceder a la trazabilidad
for paso in resultado.trazabilidad:
    print(f"Agente: {paso.agente}")
    print(f"Status: {paso.status}")
    print(f"Duración: {paso.duracion_ms}ms")
```

## Despliegue en Streamlit Cloud

1. **Preparar archivos**: Asegurarse de incluir todos los `.py` y `requirements.txt`

2. **Configurar Secrets**:
   Crear `.streamlit/secrets.toml`:
   ```toml
   [secrets]
   OPENAI_API_KEY = "sk-..."
   ```

3. **Deploy**:
   - Subir a GitHub
   - Ir a share.streamlit.io
   - Seleccionar `streamlit_app.py`

## Justificación Técnica

### Arquitectura Modular
- **Separación de responsabilidades**: Cada agente tiene una función específica
- **Prompts estructurados**: System prompts definidos para cada agente
- **Outputs tipados**: Uso de dataclasses para type safety
- **Manejo de errores**: Try-catch en cada agente

### LangChain Integration
- **Cliente LLM**: Abstracción sobre OpenAI API
- **Fallback**: Modo sin API para testing
- **Prompts**: Templates estructurados con system + user messages
- **JSON Output**: Parsing de respuestas JSON

### Beneficios
1. **Escalabilidad**: Agregar nuevos agentes es straightforward
2. **Mantenibilidad**: Código organizado y documentado
3. **Testing**: Fallback permite testing sin costos de API
4. **Trazabilidad**: Logging completo de cada paso

## Requirements

```
langchain>=0.1.0
langchain-openai>=0.0.2
streamlit>=1.28.0
pandas>=2.0.0
python-dotenv>=1.0.0
```

## Licencia

MIT
