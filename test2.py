import streamlit as st
import time

@st.fragment()
def chatbot_ui(pokemon):

    oak_avatar = "https://i.imgur.com/3vZSHwH.png"
    user_avatar = "https://i.imgur.com/h3kK4Cp.png"

    st.markdown("""
        <style>
                .st-emotion-cache-u4v75y{
                    max-height: 400px;
                    overflow-y: auto;
                     display: flex;
                    flex-direction: column-reverse;
                }
        </style>
    """, unsafe_allow_html=True)


    with st.container(border=True):
        if "history" not in st.session_state:
            st.session_state.history = []
        if "pending" not in st.session_state:
            st.session_state.pending = None  # guarda la última pregunta pendiente

        with st.chat_message("system", avatar=oak_avatar):
            st.write(f"Hey there, young trainer! I'm Professor Oak, and I've spent my life studying Pokémon. Do you want to know more about {pokemon}?")

        # Renderizar historial
        for message in st.session_state.history:
            with st.chat_message(message["role"], avatar=oak_avatar if message["role"] == "assistant" else user_avatar):
                st.write(message["content"])

        # Renderizar mientras se espera respuesta
        if st.session_state.pending:
            with st.chat_message("user", avatar=user_avatar):
                st.write(st.session_state.pending)

            with st.chat_message("system", avatar=oak_avatar):
                st.markdown(
                    f"""
                    <div style="display: flex; align-items: flex-start;">
                        <img src="https://i.imgur.com/QfGpyac.gif" 
                            alt="writing GIF" width="60" style="margin-top: -40px; margin-left: -20px;">
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        prompt = st.chat_input("Ask Professor Oak anything about Pokémon")

        if prompt:
            # el usuario manda mensaje → se muestra inmediatamente como "pendiente"
            st.session_state.pending = prompt

            st.rerun()

        # si hay un mensaje pendiente, generamos respuesta
        if st.session_state.pending:
            user_msg = st.session_state.pending
            st.session_state.history.append({"role": "user", "content": user_msg})
            
            # === Llamada al LLM (simulada aquí) ===
            # answer = chatbot.professor_oak(user_msg, pokemon)
            time.sleep(2)
            answer = "Your mission is to educate, inspire, and support trainers in their journey through the Pokémon world."
            
            st.session_state.history.append({"role": "assistant", "content": answer})
            st.session_state.pending = None
            st.rerun()

    st.button("Clear", on_click=lambda: st.session_state.update({"history": [], "pending": None}))



chatbot_ui("pikachu")