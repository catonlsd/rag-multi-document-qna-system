# 📚 RAG-Based Multi-Document QnA System

A full-stack AI-powered document question-answering system that allows users to upload multiple PDFs and ask questions across them using Retrieval-Augmented Generation.

The system uses hybrid retrieval, reranking, conversational memory, streaming responses, and source citations.

---

## 🚀 Features

- Multi-PDF upload
- PDF text extraction
- Smart text chunking
- Sentence Transformer embeddings
- FAISS vector database
- BM25 keyword search
- Hybrid retrieval
- Cross-Encoder reranking
- Groq LLM integration
- Streaming AI responses
- Conversational memory
- Source citations with page numbers
- Knowledge base stats
- Duplicate PDF prevention
- Reset knowledge base
- Modern Next.js frontend
- FastAPI backend

---

# 🧠 How It Works

1. Users upload one or more PDF documents.
2. PDF text is extracted using PyMuPDF.
3. Extracted text is split into overlapping chunks.
4. Sentence Transformers generate semantic embeddings.
5. Chunks are stored in a FAISS vector database.
6. BM25 performs keyword-based retrieval.
7. Hybrid retrieval combines semantic and keyword search.
8. Cross-Encoder reranks retrieved chunks.
9. Groq LLM generates contextual answers.
10. Answers stream in real time with source citations.

---

#  System Architecture

```text
User Uploads PDFs
        │
        ▼
PDF Text Extraction (PyMuPDF)
        │
        ▼
Text Chunking
        │
        ▼
Sentence Transformer Embeddings
        │
        ▼
┌──────────────────────────┐
│      Hybrid Retrieval    │
│ ┌────────┐  ┌─────────┐  │
│ │ FAISS  │  │  BM25   │  │
│ └────────┘  └─────────┘  │
└──────────────┬───────────┘
               ▼
Cross-Encoder Reranking
               ▼
Groq LLM Generation
               ▼
Streaming AI Responses
               ▼
Answer + Source Citations

---

🛠️ Tech Stack
->Backend
Python
FastAPI
Uvicorn
PyMuPDF
FAISS
Rank-BM25
Sentence Transformers
Cross-Encoder
Groq API

->Frontend
Next.js
TypeScript
Tailwind CSS
Axios
React Markdown
Lucide React

->AI / NLP Concepts
Retrieval-Augmented Generation (RAG)
Semantic Search
Hybrid Search
Dense Retrieval
Sparse Retrieval
Vector Similarity Search
Conversational Memory
Cross-Encoder Reranking

---

# 📂 Project Structure

rag_multi_doc_qna/
│
├── backend/
│   │
│   ├── .env
│   ├── .gitignore
│   ├── document_tracker.py
│   ├── llm_service.py
│   ├── main.py
│   ├── pdf_processor.py
│   ├── requirements.txt
│   ├── retriever.py
│   ├── text_splitter.py
│   └── vector_store.py
│
├── frontend_nextjs/
│   │
│   ├── .next/
│   ├── node_modules/
│   ├── public/
│   │
│   ├── src/
│   │   └── app/
│   │       ├── favicon.ico
│   │       ├── globals.css
│   │       ├── layout.tsx
│   │       └── page.tsx
│   │
│   ├── .gitignore
│   ├── eslint.config.mjs
│   ├── next-env.d.ts
│   ├── next.config.ts
│   ├── package-lock.json
│   ├── package.json
│   ├── postcss.config.mjs
│   ├── README.md
│   └── tsconfig.json
│
├── frontend_streamlit/
│
├── .gitattributes
├── .gitignore
└── README.md

---

⚙️ Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/catonlsd/rag-multi-document-qna-system.git
cd rag_multi_doc_qna
```

---

2️⃣ Backend Setup

Navigate to backend directory:

cd backend

Create virtual environment:
---
Windows
python -m venv venv
venv\Scripts\activate
---
Mac/Linux
python3 -m venv venv
source venv/bin/activate
---
Install dependencies:

pip install -r requirements.txt
---
Create .env file:

GROQ_API_KEY=YOUR_GROQ_API_KEY
---
Run backend server:

python -m uvicorn main:app --reload
---
Backend runs at:

http://127.0.0.1:8000

---


3️⃣ Frontend Setup

Navigate to frontend:
cd frontend_nextjs
---
Install dependencies:
npm install
---
Run frontend:
npm run dev
---
Frontend runs at:
http://localhost:3000

---

🔌 API Endpoints

GET /health
Returns backend health status.
---
GET /stats
Returns knowledge base statistics.
---
GET /documents
Returns uploaded documents.
---
POST /upload
Uploads and processes PDF documents.
---
POST /ask
Generates contextual answers using RAG.
Example Request
{
  "query": "Explain CI/CD in detail"
}
---
POST /ask-stream
Streams AI-generated answers token-by-token.
---
DELETE /reset
Resets the vector database and uploaded documents.

---


💬 Example Queries
1.Explain CI/CD in detail.
2.What is Kubernetes?
3.Compare Docker and Virtual Machines.
4.Explain Retrieval-Augmented Generation.
5.Summarize the uploaded DevOps document.

---


What are vector databases?
🧠 AI Concepts Used
Retrieval-Augmented Generation (RAG)
Semantic Search
Hybrid Retrieval
Dense + Sparse Retrieval
Cross-Encoder Reranking
Conversational Context Injection
Vector Databases
Streaming LLM Responses

---


🔒 Hallucination Reduction Strategy
The system reduces hallucinations using:

document-grounded retrieval
reranking
prompt engineering
contextual chunk selection
source-based answering
---
The LLM is explicitly instructed to:

answer only from retrieved context
avoid assumptions
mention insufficient information when necessary


---

📈 Future Improvements
PDF preview viewer
Citation click navigation
Persistent chat history
User authentication
Multi-user support
Docker deployment
Cloud deployment
OCR support for scanned PDFs
Semantic caching
Agentic RAG workflows
Voice input support
Multi-modal RAG

---


📄 Resume Description

Built a full-stack AI-powered Retrieval-Augmented Generation (RAG) system using FastAPI, Next.js, FAISS, BM25, Sentence Transformers, and Groq LLM. Implemented semantic document retrieval, hybrid search, Cross-Encoder reranking, conversational memory, streaming AI responses, source citations, markdown rendering, and a responsive SaaS-style frontend interface for intelligent multi-document question answering.

👨‍💻 Author

Mokshit