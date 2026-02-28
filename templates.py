TEMPLATE_NAMES = {
    "ingeniero_ml": "Ingeniero de Machine Learning",
    "data_scientist": "Cientifico de Datos",
    "software_engineer_ai": "Ingeniero de Software AI",
    "fullstack_developer": "Desarrollador Full Stack",
    "experto_ciberseguridad": "Experto en Ciberseguridad",
    "frontend_developer": "Desarrollador Frontend",
    "backend_developer": "Desarrollador Backend",
}

STACKS_REQUERIDOS = {
    "ingeniero_ml": [
        "Python",
        "TensorFlow",
        "PyTorch",
        "Scikit-learn",
        "SQL",
        "Docker",
        "AWS",
        "MLflow",
        "Kubernetes",
        "pandas",
        "NumPy",
    ],
    "data_scientist": [
        "Python",
        "R",
        "SQL",
        "Pandas",
        "NumPy",
        "Tableau",
        "Machine Learning",
        "Statistical Analysis",
        "Jupyter",
        "Power BI",
    ],
    "software_engineer_ai": [
        "Python",
        "LangChain",
        "LangChain-Architecture",
        "LangChain-Orchestration",
        "OpenAI",
        "FastAPI",
        "Vector Database",
        "Docker",
        "Git",
        "REST APIs",
        "Pinecone",
        "Weaviate",
        "Chroma",
        "LLM",
        "RAG",
    ],
    "fullstack_developer": [
        "JavaScript",
        "React",
        "Node.js",
        "Python",
        "PostgreSQL",
        "Docker",
        "Git",
        "REST APIs",
        "TypeScript",
        "Next.js",
    ],
    "experto_ciberseguridad": [
        "Penetration Testing",
        "Python",
        "Linux",
        "Firewalls",
        "SIEM",
        "Network Security",
        "Incident Response",
        "Metasploit",
    ],
    "frontend_developer": [
        "JavaScript",
        "TypeScript",
        "React",
        "CSS",
        "HTML",
        "Tailwind",
        "Git",
        "REST APIs",
        "Next.js",
        "Vue.js",
    ],
    "backend_developer": [
        "Python",
        "Node.js",
        "PostgreSQL",
        "Docker",
        "REST APIs",
        "Git",
        "AWS",
        "FastAPI",
        "MongoDB",
    ],
}

NIVELES_DEFAULT = {
    "ingeniero_ml": "senior",
    "data_scientist": "semi-senior",
    "software_engineer_ai": "senior",
    "fullstack_developer": "senior",
    "experto_ciberseguridad": "senior",
    "frontend_developer": "semi-senior",
    "backend_developer": "senior",
}

EXPERIENCIA_MINIMA = {
    "ingeniero_ml": 3,
    "data_scientist": 2,
    "software_engineer_ai": 3,
    "fullstack_developer": 3,
    "experto_ciberseguridad": 3,
    "frontend_developer": 2,
    "backend_developer": 3,
}

TEMPLATES_CV = {
    "software_engineer_ai": """
NOMBRE COMPLETO
Ingeniero de Software AI

RESUMEN PROFESIONAL:
Ingeniero de software especializado en la integracion de capacidades de IA en aplicaciones de produccion. [X] anos de experiencia combinando desarrollo de software robusto con conocimientos de ML y LLMs.

EXPERIENCIA PROFESIONAL:
[X] anos de experiencia en AI Engineering

HABILIDADES TECNICAS:
Lenguajes y Frameworks:
- Python, TypeScript, Go, Java
- LangChain, LangChain-Architecture, LangChain-Orchestration
- LlamaIndex, AutoGen, CrewAI
- FastAPI, Flask, Django

LLMs y AI:
- OpenAI API (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Hugging Face, Local Models
- Prompt Engineering, RAG Architecture

Bases de Datos:
- Vector DBs: Pinecone, Weaviate, Chroma, FAISS
- PostgreSQL, MongoDB, Redis

Cloud y DevOps:
- AWS, GCP, Azure
- Docker, Kubernetes
- CI/CD, GitHub Actions

EXPERIENCIA LABORAL:
- AI Software Engineer en [Empresa] (202X-presente)
- Backend Developer en [Empresa Anterior] (202X-202X)
- Full Stack Developer (202X-202X)

EDUCACION:
- Ingenieria en Sistemas, Ciencias de la Computacion
- Especializacion en Inteligencia Artificial
- Certificaciones: LangChain LLM Apps, AWS AI Practitioner, OpenAI Developer

PROYECTOS DESTACADOS:
- Chatbot empresarial con RAG personalizado
- Agentes AI para automatizacion de procesos
- Integracion de LLMs en aplicaciones existentes
- Pipeline de embeddings para busqueda semantica
""",
    "ingeniero_ml": """
NOMBRE COMPLETO
Ingeniero de Machine Learning

RESUMEN PROFESIONAL:
Profesional especializado en el diseno, desarrollo y despliegue de modelos de aprendizaje automatico a escala de produccion. [X] anos de experiencia en el sector.

EXPERIENCIA PROFESIONAL:
[X] anos de experiencia en Machine Learning

HABILIDADES TECNICAS:
- Lenguajes: Python, R, Scala, Julia
- ML/DL: TensorFlow, PyTorch, Keras, Scikit-learn, XGBoost
- MLOps: MLflow, Kubeflow, SageMaker, Vertex AI
- Bases de datos: PostgreSQL, MongoDB, Redis
- Cloud: AWS (SageMaker), GCP (Vertex AI), Azure ML
- Docker, Kubernetes, Git
- NLP: Transformers, BERT, spaCy, NLTK
- Computer Vision: OpenCV, YOLO, ResNet

EXPERIENCIA LABORAL:
- Ingeniero ML en [Empresa] (202X-presente)
- ML Engineer en [Empresa Anterior] (202X-202X)

EDUCACION:
- Maestria/PhD en Ciencias de la Computacion
- Certificaciones: AWS ML Specialty, GCP ML Engineer

PROYECTOS DESTACADOS:
- Desarrollo de modelos de recomendacion para producto
- Implementacion de pipelines de ML en produccion
- Optimizacion de modelos para inferencia en tiempo real
""",
    "data_scientist": """
NOMBRE COMPLETO
Cientifico de Datos

RESUMEN PROFESIONAL:
Cientifico de datos con [X] anos de experiencia en analisis estadistico, modelado predictivo y visualizacion de datos.

EXPERIENCIA PROFESIONAL:
[X] anos de experiencia en Data Science

HABILIDADES TECNICAS:
- Python, R, SQL, Scala
- Pandas, NumPy, SciPy, Scikit-learn
- TensorFlow, PyTorch (basico)
- Tableau, Power BI, Looker, Matplotlib, Seaborn
- Big Data: Spark, Hadoop, Hive
- Cloud: AWS, GCP, Azure

EXPERIENCIA LABORAL:
- Data Scientist en [Empresa] (202X-presente)
- Analista de Datos en [Empresa Anterior] (202X-202X)

EDUCACION:
- Maestria en Estadistica, Ciencia de Datos, Matematicas
""",
    "fullstack_developer": """
NOMBRE COMPLETO
Desarrollador Full Stack

RESUMEN PROFESIONAL:
Desarrollador full stack con [X] anos de experiencia en el desarrollo de aplicaciones web completas.

EXPERIENCIA PROFESIONAL:
[X] anos de experiencia en desarrollo full stack

HABILIDADES TECNICAS:
Frontend:
- JavaScript, TypeScript, HTML5, CSS3
- React, Vue.js, Angular, Svelte
- Next.js, Redux, Tailwind CSS

Backend:
- Node.js, Python, Java, Go
- Express, Django, FastAPI, Spring Boot
- PostgreSQL, MySQL, MongoDB, Redis

DevOps:
- Docker, Kubernetes
- AWS, GCP, Azure
- CI/CD, Git
""",
    "experto_ciberseguridad": """
NOMBRE COMPLETO
Experto en Ciberseguridad

RESUMEN PROFESIONAL:
Profesional de ciberseguridad con [X] anos de experiencia en proteccion de sistemas, redes y datos.

EXPERIENCIA PROFESIONAL:
[X] anos de experiencia en Ciberseguridad

HABILIDADES TECNICAS:
Ofensiva:
- Penetration Testing, Ethical Hacking
- Metasploit, Burp Suite, Nmap, Wireshark
- Exploit development, Reverse Engineering

Defensiva:
- SIEM, SOC Operations
- Firewalls, IDS/IPS
- Incident Response, Forensic Analysis

Cumplimiento:
- ISO 27001, NIST, OWASP
- GDPR, HIPAA, PCI-DSS
""",
    "frontend_developer": """
NOMBRE COMPLETO
Desarrollador Frontend

RESUMEN PROFESIONAL:
Desarrollador frontend con [X] anos de experiencia especializado en interfaces modernas.

HABILIDADES TECNICAS:
- JavaScript, TypeScript
- React, Vue.js, Angular, Svelte
- Next.js, Tailwind CSS
- Jest, Cypress
- Webpack, Vite
""",
    "backend_developer": """
NOMBRE COMPLETO
Desarrollador Backend

RESUMEN PROFESIONAL:
Desarrollador backend con [X] anos de experiencia en APIs y microservicios.

HABILIDADES TECNICAS:
- Python, Node.js, Go, Java
- Django, FastAPI, Express, Spring Boot
- PostgreSQL, MongoDB, Redis
- AWS, Docker, Kubernetes
- REST, GraphQL, gRPC
""",
}
