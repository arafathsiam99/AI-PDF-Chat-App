# 📄 AI PDF Chat Application

> A production-ready RAG-based document intelligence platform with voice input, risk analysis, and meeting minutes generation.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0-red)
![LangChain](https://img.shields.io/badge/LangChain-Latest-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌐 Live Demo
**[https://ai-pdf-chat-groq.streamlit.app](https://ai-pdf-chat-groq.streamlit.app)**

---

## ✨ Features

| Feature | Description |
|---|---|
| 💬 **AI Chat** | Chat with multiple PDFs using RAG |
| 🔍 **Semantic Search** | Search through documents semantically |
| ⚠️ **Risk Analyzer** | AI-powered risk detection for legal/medical/financial docs |
| 📋 **Meeting Minutes** | Auto-generate professional meeting minutes |
| 🎤 **Voice Input** | Speech-to-text using Groq Whisper API |
| 📊 **Analytics** | Usage analytics with Plotly charts |
| 🔐 **GitHub OAuth** | Secure authentication |
| 💾 **Chat History** | Save and load conversations |

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **LLM:** Groq LLaMA 3.3 70B
- **Speech-to-Text:** Groq Whisper Large V3
- **Vector Store:** FAISS
- **Embeddings:** HuggingFace Sentence Transformers
- **Framework:** LangChain
- **Auth:** GitHub OAuth
- **Deployment:** Streamlit Cloud

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Groq API Key (free at [console.groq.com](https://console.groq.com))
- GitHub OAuth App credentials

### Installation

```bash
# Clone the repository
git clone https://github.com/arafathsiam99/AI-PDF-Chat-App.git
cd AI-PDF-Chat-App

# Create virtual environment
conda create -n pdf_chat python=3.11
conda activate pdf_chat

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file:
```env
GROQ_API_KEY=your_groq_api_key
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
```

### Run

```bash
streamlit run app.py
```

---

## 📁 Project Structure
pdf_chat/
├── app.py                 # Main application
├── auth.py                # GitHub OAuth authentication
├── analytics.py           # Analytics dashboard
├── utils/
│   ├── pdf_processor.py   # PDF text extraction
│   └── chat_engine.py     # LangChain RAG engine
├── requirements.txt
└── .env
---

## 🔧 How It Works
PDF Upload → Text Extraction → Chunking → Embeddings → FAISS Index
↓
User Question → Embedding → Similarity Search → Context + LLM → Answer

---

## 📸 Screenshots


### 💬 Chat Interface
> Upload PDFs and chat with AI in natural language

### ⚠️ Risk Analyzer
> AI detects risks, red flags, and critical dates in documents

### 📋 Meeting Minutes
> Auto-generate professional minutes from any document

### 📊 Analytics Dashboard
> Track usage with interactive Plotly charts

---

## 👤 Author

**Arafath Siam**
- GitHub: [@arafathsiam99](https://github.com/arafathsiam99)

---

## ⭐ If you found this helpful, please star the repository!
