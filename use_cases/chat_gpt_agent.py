
import os
from dotenv import load_dotenv
import streamlit as st
from autogen import AssistantAgent

# Fondo con imagen usando base64
import base64
from pathlib import Path

def get_base64(file_path):
    return base64.b64encode(Path(file_path).read_bytes()).decode()

# Ruta robusta para cualquier sistema operativo
img_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'muelitaSmile.jpg')
img_base64 = get_base64(img_path)
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url('data:image/jpg;base64,{img_base64}');
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        color: rgb(105, 6, 6);
    }}
    .stMarkdown, .stTextInput, .stButton, .stTitle, .stSubheader {{
        color: rgb(105, 6, 6) !important;
    }}
    .main-flex-container {{
        display: flex;
        flex-direction: row;
        width: 100vw;
        height: 100vh;
        gap: 0;
    }}
    .main-col1 {{
        flex: 1;
        padding: 2vw;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        justify-content: flex-start;
    }}
    .main-col2 {{
        flex: 1;
        padding: 2vw;
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        justify-content: flex-start;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Contenedor principal flex para manipulación independiente
st.markdown(
    """
    <div class='main-flex-container'>
        <div class='main-col1'>
    """,
    unsafe_allow_html=True
)
    # Columna 1
st.subheader("Información adicional")
st.write("Aquí puedes mostrar datos, instrucciones, o cualquier otro contenido que desees.")
st.image("dentistDalia.jpg", caption="Imagen: dentistDal", use_container_width=True)
fecha_seleccionada = st.date_input("Selecciona una fecha:")

st.markdown("</div><div class='main-col2'>", unsafe_allow_html=True)

# Columna 2
st.title("Chat con GPT-The office")
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

st.markdown(
    """
    <style>
    label[for='user_input'], .st-emotion-cache-1qg05tj {
        color: rgb(105, 6, 6) !important;
        font-weight: bold !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
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

        st.markdown("</div></div>", unsafe_allow_html=True)
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

    st.markdown("</div>", unsafe_allow_html=True)