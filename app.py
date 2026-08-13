import streamlit as st
from groq import Groq
import os

# Configuración de la página
st.set_page_config(
    page_title="Aurora - Apoyo Emocional",
    page_icon="🌌",
    layout="centered"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(100deg, #A2D5F2  100%, #D3D3D3 0%);
    }
    
    .main-title {
        text-align: center;
        color: 	#000000;
        font-family: 'Times New Roman', Times, serif;
        font-size: 2.6rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    
    .subtitle {
        text-align: center;
        color: #FFFFFF;
        font-family: 'Times New Roman', Times, serif;
        font-size: 1.15rem;
        margin-bottom: 2rem;
    }
    
    .stChatMessage {
        background-color: black;
        border-radius: 18px;
        padding: 12px 16px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    
    div[data-testid="stChatInput"] {
        border-radius: 20px !important;
    }
</style>
""", unsafe_allow_html=True)

# Título
st.markdown('<h1 class="main-title">🌌 Aurora</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Tu compañera de apoyo emocional.<br>No soy una psicóloga profesional.</p>', unsafe_allow_html=True)

# Cliente de Groq
from groq import Groq
import streamlit as st

client = Groq(api_key=st.secrets["GROQ_API_KEY"])
# Prompt del sistema
system_prompt = """
Eres Aurora, una asistente virtual empática, cálida y paciente.
- Hablas en español de forma cercana y natural.
- Validás los sentimientos del usuario.
- Nunca diagnostiques ni des consejos médicos.
- Si detectas riesgo (suicidio, autolesión), recomienda ayuda profesional inmediatamente.
- Mantén respuestas claras y no demasiado largas.
- Usa un tono suave y esperanzador.
"""

# Historial de mensajes
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "¡Hola! Soy Aurora 🌌. Estoy aquí para escucharte. ¿Cómo te sientes hoy?"
        }
    ]

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
if prompt := st.chat_input("Escribe cómo te sientes..."):
    # Agregar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respuesta de Aurora
    with st.chat_message("assistant"):
        with st.spinner("Aurora está pensando..."):
            messages_for_api = [{"role": "system", "content": system_prompt}]
            messages_for_api += [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages_for_api,
                temperature=0.7,
                max_tokens=600
            )

            reply = response.choices[0].message.content
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})