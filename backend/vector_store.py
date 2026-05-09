import os
import pickle
import faiss
import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

VECTOR_DB_DIR = "vector_db"
INDEX_PATH = os.path.join(VECTOR_DB_DIR, "faiss_index.bin")
CHUNKS_PATH = os.path.join(VECTOR_DB_DIR, "chunks.pkl")
BM25_PATH = os.path.join(VECTOR_DB_DIR, "bm25.pkl")

os.makedirs(VECTOR_DB_DIR, exist_ok=True)

index = None
stored_chunks = []
bm25_index = None
tokenized_corpus = []


def tokenize(text):
    return text.lower().split()


def build_bm25_index():
    global bm25_index, tokenized_corpus

    tokenized_corpus = [
        tokenize(chunk["content"])
        for chunk in stored_chunks
    ]

    if tokenized_corpus:
        bm25_index = BM25Okapi(tokenized_corpus)
    else:
        bm25_index = None


def load_vector_store():
    global index, stored_chunks, bm25_index, tokenized_corpus

    if os.path.exists(INDEX_PATH) and os.path.exists(CHUNKS_PATH):
        index = faiss.read_index(INDEX_PATH)

        with open(CHUNKS_PATH, "rb") as f:
            stored_chunks = pickle.load(f)

        if os.path.exists(BM25_PATH):
            with open(BM25_PATH, "rb") as f:
                bm25_index, tokenized_corpus = pickle.load(f)
        else:
            build_bm25_index()

        return {
            "loaded": True,
            "total_vectors": index.ntotal,
            "total_chunks": len(stored_chunks)
        }

    return {
        "loaded": False,
        "total_vectors": 0,
        "total_chunks": 0
    }


def save_vector_store():
    if index is not None:
        faiss.write_index(index, INDEX_PATH)

        with open(CHUNKS_PATH, "wb") as f:
            pickle.dump(stored_chunks, f)

        with open(BM25_PATH, "wb") as f:
            pickle.dump((bm25_index, tokenized_corpus), f)


def add_chunks_to_vector_store(chunks):
    global index, stored_chunks

    texts = [chunk["content"] for chunk in chunks]

    embeddings = embedding_model.encode(texts)
    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]

    if index is None:
        index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)
    stored_chunks.extend(chunks)

    build_bm25_index()
    save_vector_store()

    return {
        "total_vectors": index.ntotal,
        "new_chunks_added": len(chunks),
        "embedding_dimension": dimension
    }