import os
import json

TRACKER_PATH = "vector_db/documents.json"

def load_documents():
    if not os.path.exists(TRACKER_PATH):
        return []

    with open(TRACKER_PATH, "r") as f:
        return json.load(f)

def save_documents(documents):
    with open(TRACKER_PATH, "w") as f:
        json.dump(documents, f, indent=4)

def is_document_processed(filename):
    documents = load_documents()
    return filename in documents

def mark_document_processed(filename):
    documents = load_documents()

    if filename not in documents:
        documents.append(filename)
        save_documents(documents)