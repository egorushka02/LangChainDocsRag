import os
import requests
import uuid
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


BACKEND_URL = os.getenv("BACKEND_URL")


st.set_page_config(page_title="LangChain RAG Chat", page_icon="🦜")

st.title("🦜 LangChain RAG Chat")


if "session_id" not in st.session_state or not st.session_state.session_id:
    st.session_state.session_id = str(uuid.uuid4())

with st.sidebar:
    st.markdown("**Model**")
    model = st.selectbox(
        "Select a model",
        options=["openai/gpt-oss-120b:free"],
        index=0,
    )
    # st.text_input("Session ID", value=st.session_state.session_id, disabled=True)
    # st.caption("Backend: " + BACKEND_URL)


st.write("Ask a question about LangChain documentation.")


if "history" not in st.session_state:
    st.session_state.history = []


for q, a in st.session_state.history:
    with st.chat_message("user"):
        st.markdown(q)
    with st.chat_message("assistant"):
        st.markdown(a)

prompt = st.chat_input("Type your question and press Enter")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    payload = {
        "question": prompt,
        "session_id": st.session_state.session_id,
        "model": model,
    }
    try:
        resp = requests.post(f"{BACKEND_URL}/chat", json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        answer = data.get("answer", "")
        st.session_state.history.append((prompt, answer))
        with st.chat_message("assistant"):
            st.markdown(answer)
    except requests.RequestException as e:
        st.error(f"Request error: {e}")


pass


