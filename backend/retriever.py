import numpy as np
import vector_store
from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def retrieve_relevant_chunks(query, top_k=5, semantic_k=10, keyword_k=10):
    if vector_store.index is None or not vector_store.stored_chunks:
        return []

    candidates = {}

    # 1. Semantic search using FAISS
    query_embedding = vector_store.embedding_model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    distances, semantic_indices = vector_store.index.search(query_embedding, semantic_k)

    for idx in semantic_indices[0]:
        if idx != -1 and idx < len(vector_store.stored_chunks):
            candidates[idx] = vector_store.stored_chunks[idx]

    # 2. Keyword search using BM25
    if vector_store.bm25_index is not None:
        tokenized_query = vector_store.tokenize(query)
        bm25_scores = vector_store.bm25_index.get_scores(tokenized_query)

        top_keyword_indices = np.argsort(bm25_scores)[::-1][:keyword_k]

        for idx in top_keyword_indices:
            if idx < len(vector_store.stored_chunks):
                candidates[idx] = vector_store.stored_chunks[idx]

    if not candidates:
        return []

    candidate_chunks = list(candidates.values())

    # 3. Cross-encoder reranking
    pairs = [
        [query, chunk["content"]]
        for chunk in candidate_chunks
    ]

    scores = reranker.predict(pairs)

    reranked = sorted(
        zip(candidate_chunks, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [chunk for chunk, score in reranked[:top_k]]