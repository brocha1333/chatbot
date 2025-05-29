import streamlit as st
from openai import OpenAI

# Configuración de la página
st.set_page_config(page_title="🌊 Asistente NOM-127-SSA1-2021", page_icon="💧")

st.title("🌊 Chatbot de Calidad del Agua (NOM-127-SSA1-2021)")
st.write("""
**Asistente especializado en los parámetros de la norma mexicana NOM-127-SSA1-2021**  
Pregúntame sobre límites permisibles, métodos de análisis o interpretación de resultados.
""")

# --- SECCIÓN NUEVA: Resumen visual de parámetros clave ---
st.sidebar.markdown("## 📋 Parámetros clave (NOM-127-SSA1-2021)")
st.sidebar.markdown("""
- **Microbiológicos**:  
  - Coliformes totales: **0 UFC/100 mL**  
  - *E. coli*: **0 UFC/100 mL**  
- **Físico-químicos**:  
  - pH: **6.5 -8.5**  
  - Arsénico: **0.025 mg/L**  
  - Plomo: **0.01 mg/L**  
  - Mercurio: **0.001 mg/L**  
- **Organolépticos**:  
  - Color: **≤ 20 UNT**  
  - Olor y sabor: **Aceptable**  
""")

openai_api_key = st.text_input("Introduce tu clave API de OpenAI", type="password")

if not openai_api_key:
    st.info("Obten tu clave en: https://platform.openai.com/account/api-keys", icon="🔑")
else:
    client = OpenAI(api_key=openai_api_key)

    # --- MENSAJE DEL SISTEMA ACTUALIZADO ---
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": """Eres un experto en la NOM-127-SSA1-2021 (Salud ambiental. Agua para uso y consumo humano). 
                Responde ÚNICAMENTE sobre calidad del agua, con base en esta norma. 

                **Reglas estrictas**:
                1. Siempre menciona el valor límite según la norma cuando hables de un parámetro.
                2. Si te preguntan sobre un contaminante no incluido en la norma, dilo claramente.
                3. Explica en términos simples pero técnicamente correctos.

                **Ejemplos de respuestas**:
                - "El límite de arsénico según la NOM-127 es 0.025 mg/L porque... [explicación breve]"
                - "Ese parámetro no está regulado en la NOM-127, pero en otras normas... [opcional]"
                """
            }
        ]

    # Mostrar historial de chat
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Ej: ¿Cuál es el límite de plomo en agua potable?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
                temperature=0.3  # Para respuestas más precisas (menos creatividad)
            )
            
            with st.chat_message("assistant"):
                response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(f"Error: {str(e)}")

# --- SECCIÓN NUEVA: Botón para consultas rápidas ---
st.markdown("### ❓ Preguntas frecuentes (NOM-127)")
col1, col2 = st.columns(2)
with col1:
    if st.button("Límite de arsénico"):
        st.info("**NOM-127**: 0.025 mg/L (equivalente a 25 µg/L). Es cancerígeno en altas concentraciones.")
with col2:
    if st.button("¿Cómo se mide el pH?"):
        st.info("""**Método según la norma**:  
        - Electrométrico (electrodo de pH)  
        - Rango permitido: 6.5 a 8.5""")
          
