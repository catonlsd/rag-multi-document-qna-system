---
title: rag-multi-document-qna-system
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

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
│   ├── main.py
│   ├── llm_service.py
│   ├── retriever.py
│   ├── vector_store.py
│   ├── pdf_processor.py
│   ├── text_splitter.py
│   ├── document_tracker.py
│   ├── requirements.txt
│   ├── uploads/
│   └── vector_db/
│
├── frontend_nextjs/
│   ├── src/
│   │   └── app/
│   │       └── page.tsx
│   ├── package.json
│   └── public/
│
├── frontend_streamlit/
│
├── screenshots/
│   ├── dashboard.png
│   ├── streaming.png
│   └── sources.png
│
├── .gitignore
└── README.md

