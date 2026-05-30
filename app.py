import streamlit as st
from utils.pdf_processor import extract_text_from_pdf, split_text_into_chunks
from utils.chat_engine import create_vector_store, create_chat_chain

st.set_page_config(page_title="PDF Chat AI", page_icon="📄")
st.title("📄 Chat with your PDF!")

# PDF Upload
uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

if uploaded_file:
    with st.spinner("PDF Processing........."):
        text = extract_text_from_pdf(uploaded_file)
        chunks = split_text_into_chunks(text)
        vector_store = create_vector_store(chunks)
        chain = create_chat_chain(vector_store)
        st.session_state.chain = chain
        st.success("PDF ready! Now Ask Question.......!")

# Chat History দেখাও
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User Input
if question := st.chat_input("ASK a question about PDF..."):
    if "chain" not in st.session_state:
        st.warning("Upload a PDF fist!")
    else:
        # User message দেখাও
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        # AI response নাও
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.chain({"question": question})
                answer = response["answer"]
                st.write(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})