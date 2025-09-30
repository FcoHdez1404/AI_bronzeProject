
import os
from dotenv import load_dotenv
import streamlit as st
from autogen import AssistantAgent

# Fondo con imagen usando base64
import base64
from pathlib import Path

def get_base64(file_path):
    return base64.b64encode(Path(file_path).read_bytes()).decode()

img_base64 = get_base64("static/muelitaSmile.jpg")
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url('data:image/jpg;base64,{img_base64}');
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

load_dotenv()

# Configuración del modelo
llm_config = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "api_key": os.environ["OPENAI_API_KEY"],
}

# Crear el agente de chat
chat_agent = AssistantAgent(
    name="Chat_Agent",
    llm_config=llm_config,
    system_message="Eres un asistente útil y conversacional."
)


# Dividir la pantalla en dos columnas verticales
col1, col2 = st.columns(2)


with col1:
    st.subheader("Información adicional")
    st.write("Aquí puedes mostrar datos, instrucciones, o cualquier otro contenido que desees.")
    st.image("dentistDalia.jpg", caption="Imagen: dentistDal", use_container_width=True)

with col2:
    st.title("Chat con GPT-The office")
    # Inicializar historial de chat
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    def enviar_mensaje():
        user_input = st.session_state.get("user_input", "")
        if user_input.strip() != "":
            messages = [{"role": "user", "content": user_input}]
            if hasattr(chat_agent, "generate_oai_reply"):
                response = chat_agent.generate_oai_reply(messages, "User")
            elif hasattr(chat_agent, "generate_llm_reply"):
                response = chat_agent.generate_llm_reply(messages, "User")
            else:
                response = "El agente no soporta chat directo."
            if isinstance(response, dict) and "content" in response:
                reply = response["content"]
            else:
                reply = str(response)
            st.session_state.chat_history.append(("Tú", user_input))
            st.session_state.chat_history.append(("Agente", reply))
            st.session_state.user_input = ""  # Limpiar input

    user_input = st.text_input(
        "Escribe tu mensaje:",
        value=st.session_state.get("user_input", ""),
        key="user_input",
        on_change=enviar_mensaje
    )

    st.markdown(
        """
        <style>
        div.stButton > button:first-child {
            background-color: #1E90FF;
            color: white;
            border: none;
            height: 3em;
            width: 100%;
            border-radius: 8px;
            font-size: 1.1em;
            font-weight: bold;
            transition: background-color 0.2s;
        }
        div.stButton > button:first-child:hover {
            background-color: #1565c0;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    if st.button("Enviar mensaje"):
        enviar_mensaje()

    st.subheader("Conversación:")
    for speaker, msg in st.session_state.chat_history:
        st.markdown(f"**{speaker}:** {msg}")