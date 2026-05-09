from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import os

from pdf_processor import extract_text_from_pdf
from text_splitter import create_chunks
from vector_store import add_chunks_to_vector_store, load_vector_store
from retriever import retrieve_relevant_chunks
from llm_service import generate_answer, stream_answer
from document_tracker import (
    is_document_processed,
    mark_document_processed,
    load_documents
)

import vector_store

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_vector_store()


class AskRequest(BaseModel):
    query: str
    chat_history: list = []


UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def home():
    return {"message": "RAG Multi-Document QnA Backend is running"}


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Backend is healthy"
    }


@app.get("/stats")
def get_stats():
    total_vectors = vector_store.index.ntotal if vector_store.index is not None else 0
    total_chunks = len(vector_store.stored_chunks)
    total_documents = len(load_documents())

    return {
        "total_documents": total_documents,
        "total_chunks": total_chunks,
        "total_vectors": total_vectors
    }


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        return {
            "message": "Only PDF files are allowed.",
            "filename": file.filename
        }

    file_content = await file.read()

    if len(file_content) > MAX_FILE_SIZE:
        return {
            "message": "PDF is too large. Maximum allowed size is 10 MB.",
            "filename": file.filename
        }

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    if is_document_processed(file.filename):
        return {
            "message": "This PDF has already been processed.",
            "filename": file.filename
        }

    with open(file_path, "wb") as buffer:
        buffer.write(file_content)

    pages = extract_text_from_pdf(file_path)
    chunks = create_chunks(pages, file.filename)
    vector_info = add_chunks_to_vector_store(chunks)

    mark_document_processed(file.filename)

    return {
        "message": "PDF uploaded, processed, and stored in vector database successfully",
        "filename": file.filename,
        "total_pages": len(pages),
        "total_chunks": len(chunks),
        "vector_store": vector_info
    }


@app.post("/ask")
def ask_question(request: AskRequest):
    query = request.query
    chat_history = request.chat_history

    if not query.strip():
        return {
            "message": "Question cannot be empty.",
            "question": query,
            "answer": None,
            "sources": []
        }

    relevant_chunks = retrieve_relevant_chunks(query)

    if not relevant_chunks:
        return {
            "message": "No vector database found. Please upload a PDF first.",
            "question": query,
            "answer": None,
            "sources": []
        }

    answer = generate_answer(query, relevant_chunks, chat_history)

    sources = []

    for chunk in relevant_chunks:
        sources.append({
            "source": chunk["metadata"]["source"],
            "page": chunk["metadata"]["page"],
            "snippet": chunk["content"][:300],
            "chunk_id": chunk["metadata"].get("chunk_id")
        })

    return {
        "question": query,
        "answer": answer,
        "sources": sources
    }

@app.post("/ask-stream")
def ask_question_stream(request: AskRequest):
    query = request.query
    chat_history = request.chat_history

    if not query.strip():
        return StreamingResponse(
            iter(["Question cannot be empty."]),
            media_type="text/plain"
        )

    relevant_chunks = retrieve_relevant_chunks(query)

    if not relevant_chunks:
        return StreamingResponse(
            iter(["No vector database found. Please upload a PDF first."]),
            media_type="text/plain"
        )

    def response_generator():
        for token in stream_answer(query, relevant_chunks, chat_history):
            yield token

    return StreamingResponse(
        response_generator(),
        media_type="text/plain"
    )


@app.get("/documents")
def get_documents():
    documents = load_documents()

    return {
        "total_documents": len(documents),
        "documents": documents
    }


@app.delete("/reset")
def reset_knowledge_base():
    vector_store.index = None
    vector_store.stored_chunks = []

    files_to_delete = [
        "vector_db/faiss_index.bin",
        "vector_db/chunks.pkl",
        "vector_db/documents.json",
        "vector_db/bm25.pkl"
    ]

    for file_path in files_to_delete:
        if os.path.exists(file_path):
            os.remove(file_path)

    return {
        "message": "Knowledge base reset successfully."
    }