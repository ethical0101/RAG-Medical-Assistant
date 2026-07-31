import streamlit as st
# pyrefly: ignore [missing-import]
from utils.api import ask_question

def render_chat():
    st.subheader("💭 Chat with your assistant")

    if 'messages' not in st.session_state:
        st.session_state.messages=[]

    #render existing chat history
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    #input and response
    user_input=st.chat_input("Type your question....")
    if user_input:
        #show user message
        st.chat_message("user").write(user_input)
        #add user message
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("assistant"):
            with st.spinner("MediBot is thinking..."):
                response=ask_question(user_input)
                if response.status_code==200:
                    data=response.json()
                    answer=data["response"]
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error("Failed to get response from AI assistant")



def stream_response(question):
    response=ask_question(question)
    if response.status_code == 200:
        answer=response.json().get("response","")
    else:
        answer="Error: Failed to get response from AI assistant"
    for word in answer.split():
        yield f"{word} "

    st.session_state.messages.append({"role":"assistant", "content":answer})
