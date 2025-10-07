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
   .main-grid-container {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 40px;
        width: 100vw;
        min-height: 100vh;
        align-items: flex-start;
        justify-content: center;
        padding: 40px 0;
    }}
    .main-col1 {{ 
        background: rgba(255,255,255,0.85);
        border-radius: 16px;
        padding: 32px 24px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        min-width: 340px;
        max-width: 400px;
    }}
    .main-col2 {{ 
        background: rgba(255,255,255,0.85);
        border-radius: 16px;
        padding: 32px 24px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        min-width: 340px;
        max-width: 600px;
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

st.markdown("""
<div class='main-grid-container'>
    <div class='main-col1'>
        <h2>Información adicional</h2>
        <p style='color:#1565c0;'>Aquí puedes mostrar datos, instrucciones, o cualquier otro contenido que desees.</p>
        <img src='dentistDalia.jpg' alt='Imagen: dentistDal' style='width:100%;border-radius:12px;margin-bottom:16px;'>
        <div style='margin-top:16px;'>
            <label style='font-weight:bold;'>Selecciona una fecha:</label><br>
        </div>
    </div>
    <div class='main-col2'>
        <h1 id='chat-con-gpt-the-office' style='color:#690606;font-size:44px;font-family:Source Sans Pro,sans-serif;padding:20px 0 16px 0;margin:0;'>Chat con GPT-The office</h1>
        <div style='margin-top:24px;'>
            <label for='user_input' style='color:#690606;font-weight:bold;'>Escribe tu mensaje:</label>
        </div>
        <h3 style='margin-top:32px;'>Conversación:</h3>
        <div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Renderizar componentes interactivos dentro del grid usando Streamlit
with st.container():
    main_col1, grid_col2 = st.columns([1,1])
with main_col1:
    st.subheader("Información adicional")
    st.write("Aquí puedes mostrar datos, instrucciones, o cualquier otro contenido que desees.")

    st.image("dentistDalia.jpg", caption="Imagen: dentistDal", use_container_width=True)
    # Calendario dinámico desplegable
    fecha_seleccionada = st.date_input("Selecciona una fecha:")

with grid_col2:
    # Contenedor alineado a la derecha
    st.markdown(
        """
        <style>
        .lmn-col-6 {
            width: 100% !important;
            display: flex;
            flex-direction: column;
            align-items: flex-end;
        }
        </style>
        <div class='chat lmn-col-6'>
        """,
        unsafe_allow_html=True
    )

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

    st.markdown("</div>", unsafe_allow_html=True)