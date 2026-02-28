import streamlit as st
import pandas as pd
import json

st.set_page_config(
    page_title="Evaluador de CV - Multiagente", page_icon="🤖", layout="wide"
)

from main import evaluar_cv
from templates import (
    TEMPLATES_CV,
    STACKS_REQUERIDOS,
    NIVELES_DEFAULT,
    EXPERIENCIA_MINIMA,
    TEMPLATE_NAMES,
)

st.title("🤖 Evaluador de Hojas de Vida")
st.markdown("Sistema multiagente con LangChain para evaluación de candidatos técnicos")


def main():
    with st.sidebar:
        st.header("⚙️ Configuración")

        tipo_seleccionado = st.selectbox(
            "Tipo de Profesional",
            options=list(TEMPLATE_NAMES.keys()),
            format_func=lambda x: TEMPLATE_NAMES[x],
        )

        st.markdown("---")

        stack_default = STACKS_REQUERIDOS.get(tipo_seleccionado, [])
        stack_input = st.text_area(
            "Stack requerido (comma-separated)", value=", ".join(stack_default)
        )

        nivel_default = NIVELES_DEFAULT.get(tipo_seleccionado, "senior")
        nivel = st.selectbox(
            "Nivel solicitado",
            ["junior", "semi-senior", "senior", "staff", "principal"],
            index=["junior", "semi-senior", "senior", "staff", "principal"].index(
                nivel_default
            ),
        )

        exp_minima = st.number_input(
            "Experiencia minima (años)",
            min_value=0,
            max_value=20,
            value=EXPERIENCIA_MINIMA.get(tipo_seleccionado, 3),
        )

        st.markdown("---")
        usar_api = st.checkbox("Usar OpenAI API", value=False)
        api_key = None
        if usar_api:
            api_key = st.text_input("API Key", type="password")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📄 Curriculum Vitae")

        tab1, tab2 = st.tabs(["Editor", "Templates"])

        with tab1:
            cv_input = st.text_area(
                "Pega el CV aqui",
                height=400,
                placeholder="Contenido del CV en texto plano...",
            )

        with tab2:
            st.markdown(f"**Perfil: {TEMPLATE_NAMES[tipo_seleccionado]}**")
            if st.button("Cargar Template"):
                template = TEMPLATES_CV.get(tipo_seleccionado, "")
                if template:
                    st.session_state["cv_content"] = template

        if "cv_content" in st.session_state and st.session_state["cv_content"]:
            with st.expander("Template cargado"):
                st.text(st.session_state["cv_content"][:500] + "...")

        cv_texto = cv_input or st.session_state.get("cv_content", "")

    with col2:
        st.subheader("📊 Resultados")

        if st.button("🚀 Evaluar CV", type="primary", disabled=not cv_texto):
            with st.spinner("Analizando con agentes..."):
                try:
                    stack_req = [s.strip() for s in stack_input.split(",") if s.strip()]

                    resultado = evaluar_cv(
                        cv_texto=cv_texto,
                        stack_requerido=stack_req,
                        nivel_solicitado=nivel,
                        experiencia_minima=exp_minima,
                        api_key=api_key if api_key else None,
                    )

                    st.session_state["resultado"] = resultado
                    st.session_state["evaluado"] = True

                except Exception as e:
                    st.error(f"Error: {str(e)}")

        if st.session_state.get("evaluado"):
            resultado = st.session_state.get("resultado")

            if resultado:
                match = resultado.porcentaje_match

                if match >= 80:
                    emoji, color = "✅", "green"
                elif match >= 60:
                    emoji, color = "👍", "blue"
                elif match >= 40:
                    emoji, color = "⚠️", "orange"
                else:
                    emoji, color = "❌", "red"

                st.markdown(
                    f"""
                <div style="padding:20px;background:#f0f2f6;border-radius:10px;text-align:center;">
                    <h2 style="margin:0;color:{color};">{emoji} {match}%</h2>
                    <p>Match con el perfil</p>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Seniority", resultado.seniority_estimado)
                with col_b:
                    st.metric("Coherente", "Si" if resultado.nivel_coherente else "No")

                st.markdown("### Skills Encontradas")
                if resultado.skills_encontradas:
                    st.success(", ".join(resultado.skills_encontradas))
                else:
                    st.info("No se detectaron skills")

                st.markdown("### Brechas Técnicas")
                if resultado.brechas_tecnicas:
                    for b in resultado.brechas_tecnicas:
                        st.error(f"- {b}")
                else:
                    st.success("Sin brechas detectadas")

                st.markdown("### Resumen")
                st.info(resultado.resumen_evaluacion)

                with st.expander("JSON"):
                    st.json(
                        {
                            "porcentaje_match": resultado.porcentaje_match,
                            "seniority_estimado": resultado.seniority_estimado,
                            "brechas_tecnicas": resultado.brechas_tecnicas,
                            "skills_encontradas": resultado.skills_encontradas,
                            "nivel_coherente": resultado.nivel_coherente,
                        }
                    )


if __name__ == "__main__":
    if "evaluado" not in st.session_state:
        st.session_state["evaluado"] = False
    if "cv_content" not in st.session_state:
        st.session_state["cv_content"] = ""
    if "resultado" not in st.session_state:
        st.session_state["resultado"] = None

    main()
