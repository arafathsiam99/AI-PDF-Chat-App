import streamlit as st
from utils.pdf_processor import extract_text_from_pdf, split_text_into_chunks
from utils.chat_engine import create_vector_store, create_chat_chain
from auth import login_page, logout
from analytics import show_analytics
import json
import os
from datetime import datetime

st.set_page_config(page_title="PDF Chat AI", page_icon="📄", layout="wide")

st.markdown("""
<style>
    .pdf-badge { background: #1e3a5f; color: #4a9eff; padding: 3px 10px; border-radius: 20px; font-size: 12px; margin: 2px; display: inline-block; }
    .stat-card { background: #1a1f2e; border-radius: 10px; padding: 15px; text-align: center; border: 1px solid #2d3748; }
    .summary-box { background: linear-gradient(135deg, #1e3a5f, #0d2137); border-left: 4px solid #4a9eff; padding: 15px; border-radius: 8px; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

for key, val in {"logged_in": False, "username": "", "avatar": "", "messages": [], "chain": None, "pdf_names": [], "summaries": {}, "page": "chat"}.items():
    if key not in st.session_state:
        st.session_state[key] = val

if not st.session_state.logged_in:
    login_page()
    st.stop()

col_title, col_nav, col_user = st.columns([2, 2, 1])
with col_title:
    st.title("📄 AI PDF Chat")
with col_nav:
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        if st.button("💬 Chat", use_container_width=True, type="primary" if st.session_state.page == "chat" else "secondary"):
            st.session_state.page = "chat"
            st.rerun()
    with col_b:
        if st.button("🔍 Search", use_container_width=True, type="primary" if st.session_state.page == "search" else "secondary"):
            st.session_state.page = "search"
            st.rerun()
    with col_c:
        if st.button("📊 Analytics", use_container_width=True, type="primary" if st.session_state.page == "analytics" else "secondary"):
            st.session_state.page = "analytics"
            st.rerun()
with col_user:
    if st.session_state.avatar:
        st.image(st.session_state.avatar, width=35)
    st.markdown(f"👤 **{st.session_state.username}**")
    if st.button("🚪 Logout", use_container_width=True):
        logout()

st.divider()

# Semantic Search Section
if st.session_state.page == "search":
    st.title("🔍 Semantic Search")
    st.markdown("*Search through your PDFs semantically*")
    st.divider()
    
    if not st.session_state.chain:
        st.warning("⚠️ Please upload and process PDFs first from the Chat page!")
    else:
        search_query = st.text_input("🔍 Enter search query", placeholder="e.g. machine learning algorithms")
        col_a, col_b = st.columns([1, 4])
        with col_a:
            top_k = st.selectbox("Results", [3, 5, 10])
        
        if search_query:
            with st.spinner("Searching..."):
                retriever = st.session_state.chain.retriever
                results = retriever.vectorstore.similarity_search(search_query, k=top_k)
            
            st.success(f"Found {len(results)} relevant passages!")
            for i, doc in enumerate(results):
                with st.expander(f"📄 Result {i+1}"):
                    st.markdown(f'<div class="summary-box">{doc.page_content}</div>', unsafe_allow_html=True)
    st.stop()

if st.session_state.page == "analytics":
    show_analytics(st.session_state.username)
    st.stop()

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📂 Upload PDFs")
    uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)
    if uploaded_files:
        if st.button("🚀 Process PDFs", use_container_width=True, type="primary"):
            all_chunks = []
            st.session_state.pdf_names = []
            st.session_state.summaries = {}
            progress = st.progress(0)
            for i, pdf_file in enumerate(uploaded_files):
                with st.spinner(f"Processing {pdf_file.name}..."):
                    text = extract_text_from_pdf(pdf_file)
                    chunks = split_text_into_chunks(text)
                    all_chunks.extend(chunks)
                    st.session_state.pdf_names.append(pdf_file.name)
                    st.session_state.summaries[pdf_file.name] = text[:3000]
                    progress.progress((i + 1) / len(uploaded_files))
            with st.spinner("Building AI knowledge base..."):
                vector_store = create_vector_store(all_chunks)
                st.session_state.chain = create_chat_chain(vector_store)
            st.success(f"✅ {len(uploaded_files)} PDF(s) ready!")

    if st.session_state.pdf_names:
        st.subheader("📑 Loaded PDFs")
        for name in st.session_state.pdf_names:
            st.markdown(f'<span class="pdf-badge">📄 {name}</span>', unsafe_allow_html=True)
        st.subheader("📊 Stats")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="stat-card"><h3>{len(st.session_state.pdf_names)}</h3><p>PDFs</p></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="stat-card"><h3>{len(st.session_state.messages)}</h3><p>Messages</p></div>', unsafe_allow_html=True)
        st.subheader("📝 Summaries")
        for pdf_name in st.session_state.summaries:
            with st.expander(f"📄 {pdf_name}"):
                if st.button("Generate Summary", key=f"sum_{pdf_name}"):
                    if st.session_state.chain:
                        with st.spinner("Generating..."):
                            response = st.session_state.chain({"question": "Give a concise summary in 5 bullet points."})
                            st.markdown(f'<div class="summary-box">{response["answer"]}</div>', unsafe_allow_html=True)

    st.subheader("💾 Chat History")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("💾 Save", use_container_width=True):
            if st.session_state.messages:
                history = {"date": datetime.now().strftime("%Y-%m-%d %H:%M"), "user": st.session_state.username, "pdfs": st.session_state.pdf_names, "messages": st.session_state.messages}
                with open(f"chat_{st.session_state.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
                    json.dump(history, f, indent=2)
                st.success("Saved!")
    with c2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

with col2:
    st.subheader("💬 Chat")
    chat_container = st.container(height=500)
    with chat_container:
        if not st.session_state.messages:
            st.info("👆 Upload PDFs and click Process to start!")
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                st.caption(message.get("time", ""))

    if question := 
    # Voice Input
    st.markdown("**🎤 Or speak your question:**")
    audio_file = st.audio_input("🎙️ Click to record")

    if audio_file:
        with st.spinner("🎤 Converting speech to text..."):
            from groq import Groq
            import tempfile
            import os
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp.write(audio_file.getvalue())
                tmp_path = tmp.name
            with open(tmp_path, "rb") as f:
                transcription = client.audio.transcriptions.create(
                    model="whisper-large-v3",
                    file=f,
                    response_format="text"
                )
            os.unlink(tmp_path)
            transcribed = transcription
            st.success(f"📝 Heard: *{transcribed}*")

            if st.session_state.chain and transcribed:
                time_now = datetime.now().strftime("%H:%M")
                st.session_state.messages.append({"role": "user", "content": transcribed, "time": time_now})
                with st.spinner("🤔 Thinking..."):
                    response = st.session_state.chain({"question": transcribed})
                    answer = response["answer"]
                st.session_state.messages.append({"role": "assistant", "content": answer, "time": time_now})
                st.rerun()
    st.chat_input("Ask anything about your PDFs..."):
        if not st.session_state.chain:
            st.warning("⚠️ Please upload and process PDFs first!")
        else:
            time_now = datetime.now().strftime("%H:%M")
            st.session_state.messages.append({"role": "user", "content": question, "time": time_now})
            with st.spinner("🤔 Thinking..."):
                response = st.session_state.chain({"question": question})
                answer = response["answer"]
            st.session_state.messages.append({"role": "assistant", "content": answer, "time": time_now})
            st.rerun()
