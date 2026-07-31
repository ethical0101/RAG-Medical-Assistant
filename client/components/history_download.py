import streamlit as st

def render_history_download():
    if st.session_state.get("messages"):
        chat_text="\n\n\n".join([f"{msg['role'].upper()}:{msg['content']}" for msg in st.session_state.messages])
        st.download_button(label="⬇️ Download Chat History", data=chat_text, file_name="chat_history.txt", mime="text/plain")
