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

## 🧠 Architecture

```text
PDF Upload
   ↓
Text Extraction using PyMuPDF
   ↓
Smart Chunking
   ↓
Embeddings using Sentence Transformers
   ↓
FAISS Vector Store + BM25 Index
   ↓
Hybrid Retrieval
   ↓
Cross-Encoder Reranking
   ↓
Groq LLM
   ↓
Streaming Answer + Sources