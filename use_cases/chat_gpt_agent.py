import os
from dotenv import load_dotenv
import streamlit as st
from autogen import AssistantAgent

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

st.title("Chat con GPT-3.5-turbo")

# Inicializar historial de chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Escribe tu mensaje:")

if st.button("Enviar mensaje"):
    if user_input.strip() != "":
        # Construir historial de mensajes para el agente
        messages = [{"role": "user", "content": user_input}]
        # Usar generate_oai_reply o generate_llm_reply según disponibilidad
        if hasattr(chat_agent, "generate_oai_reply"):
            response = chat_agent.generate_oai_reply(messages, "User")
        elif hasattr(chat_agent, "generate_llm_reply"):
            response = chat_agent.generate_llm_reply(messages, "User")
        else:
            response = "El agente no soporta chat directo."
        # Extraer el texto de la respuesta
        if isinstance(response, dict) and "content" in response:
            reply = response["content"]
        else:
            reply = str(response)
        st.session_state.chat_history.append(("Tú", user_input))
        st.session_state.chat_history.append(("Agente", reply))

# Mostrar historial de chat
st.subheader("Conversación:")
for speaker, msg in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {msg}")