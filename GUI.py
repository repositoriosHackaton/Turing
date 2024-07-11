import streamlit as st
from victorAI import Chatbot

# Inicializando el chatbot
victor = Chatbot('API_key.env', 'Data/final_data.pdf')

# Estilizando el titulo de la pagina.
st.set_page_config(page_title="Victor el asistente", page_icon=":robot_face:", layout="centered")

st.title("Victor AI")

# Iniciando el historial del chat.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrando los mensajes del historial
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message.get("avatar")):
        st.markdown(message["content"])

# Reaccionando al input del usuario.
if prompt := st.chat_input("¿Tienes alguna consulta?"):
    # Enseñando el mensaje del usuario.
    with st.chat_message("user", avatar='Icons/UserIcon.png'):
        st.markdown(prompt)
    # Añadiendo el mensaje al historial del chat.
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar": 'Icons/UserIcon.png'})

    response = f"Victor: {victor.chat(prompt)}"
    # Enseñando la respuesta del modelo.
    with st.chat_message("assistant", avatar='Icons/VictorIcon.png'):
        st.markdown(response)
    # Añadiendo el mensaje al historial del chat.
    st.session_state.messages.append({"role": "assistant", "content": response, "avatar": 'Icons/VictorIcon.png'})