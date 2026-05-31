import streamlit as st
import json
import os
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter

def load_all_chats(username):
    chats = []
    for f in os.listdir("."):
        if f.startswith(f"chat_{username}_") and f.endswith(".json"):
            with open(f) as file:
                chats.append(json.load(file))
    return chats

def show_analytics(username):
    st.title("📊 Analytics Dashboard")
    st.markdown(f"*Usage stats for **{username}***")
    st.divider()

    chats = load_all_chats(username)

    if not chats:
        st.info("💡 No chat history yet! Start chatting to see analytics.")
        return

    total_chats = len(chats)
    total_messages = sum(len(c["messages"]) for c in chats)
    total_pdfs = sum(len(c.get("pdfs", [])) for c in chats)
    user_messages = sum(len([m for m in c["messages"] if m["role"] == "user"]) for c in chats)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("💬 Total Sessions", total_chats)
    with c2:
        st.metric("📨 Total Messages", total_messages)
    with c3:
        st.metric("📄 PDFs Analyzed", total_pdfs)
    with c4:
        st.metric("❓ Questions Asked", user_messages)

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💬 Messages per Session")
        session_labels = [f"Session {i+1}" for i in range(len(chats))]
        msg_counts = [len(c["messages"]) for c in chats]
        fig = go.Figure(go.Bar(
            x=session_labels,
            y=msg_counts,
            marker_color="#4a9eff",
            text=msg_counts,
            textposition="auto"
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            height=300,
            margin=dict(t=20, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("📄 PDF Usage")
        all_pdfs = []
        for c in chats:
            all_pdfs.extend(c.get("pdfs", []))
        if all_pdfs:
            pdf_counts = Counter(all_pdfs)
            fig2 = px.pie(
                values=list(pdf_counts.values()),
                names=list(pdf_counts.keys()),
                color_discrete_sequence=px.colors.sequential.Blues_r
            )
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="white",
                height=300,
                margin=dict(t=20, b=20)
            )
            st.plotly_chart(fig2, use_container_width=True)

    st.subheader("🕒 Recent Sessions")
    for chat in reversed(chats[-5:]):
        with st.expander(f"📅 {chat.get('date', 'Unknown')} — {len(chat['messages'])} messages"):
            st.write(f"**PDFs:** {', '.join(chat.get('pdfs', []))}")
            for msg in chat["messages"][:3]:
                role = "🧑" if msg["role"] == "user" else "🤖"
                st.write(f"{role} {msg['content'][:100]}...")
