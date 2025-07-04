from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from utils.hashing import compute_pdf_hash
from utils.vector_store import load_or_create_vector_store
from services.chat import generate_response

st.set_page_config(page_title="RAG Chatbot")
st.title("🤖 RAG Chatbot from Your PDF")

uploaded_pdf = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_pdf:
    file_bytes = uploaded_pdf.read()
    file_hash = compute_pdf_hash(file_bytes)
    collection_name = f"pdf_{file_hash[:12]}"

    if "last_file_hash" not in st.session_state or st.session_state.last_file_hash != file_hash:
        st.session_state.last_file_hash = file_hash
        st.session_state.chat_history = []
        st.session_state.vector_store = None

    st.info(f"Collection: `{collection_name}`")

    with st.spinner("⏳ Processing PDF and preparing chat..."):
        if st.session_state.vector_store is None:
            vector_store = load_or_create_vector_store(file_bytes, collection_name)
            st.session_state.vector_store = vector_store
            st.session_state.chat_history = []

if "vector_store" in st.session_state and st.session_state.vector_store:
    st.divider()
    st.header("💬 Ask questions about your PDF")

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_query = st.chat_input("Ask a question...")

    if user_query:
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.spinner("💡 Generating answer..."):
            response = generate_response(
                user_query,
                st.session_state.vector_store
            )

        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.chat_history.append({"role": "assistant", "content": response})
