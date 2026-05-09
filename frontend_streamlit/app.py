import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Multi-Document RAG QnA",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Multi-Document RAG QnA System")
st.caption("Upload multiple PDFs and ask questions across all documents.")

if "messages" not in st.session_state:
    st.session_state.messages = []


def show_sources(sources):
    with st.expander("📌 Sources"):
        unique_sources = set()

        for source in sources:
            source_text = f"{source['source']} | Page {source['page']}"

            if source_text not in unique_sources:
                unique_sources.add(source_text)
                st.markdown(f"**📄 {source_text}**")

                if source.get("snippet"):
                    st.caption(source["snippet"] + "...")


with st.sidebar:
    st.header("⚙️ System Status")

    try:
        health_response = requests.get(f"{BACKEND_URL}/health", timeout=10)

        if health_response.status_code == 200:
            st.success("Backend connected")
        else:
            st.warning("Backend issue detected")

    except requests.exceptions.ConnectionError:
        st.error("Backend offline")

    except requests.exceptions.Timeout:
        st.error("Backend timeout")

    st.divider()

    st.header("📊 Knowledge Base Stats")

    try:
        stats_response = requests.get(f"{BACKEND_URL}/stats", timeout=10)

        if stats_response.status_code == 200:
            stats = stats_response.json()

            st.metric("Documents", stats["total_documents"])
            st.metric("Chunks", stats["total_chunks"])
            st.metric("Vectors", stats["total_vectors"])
        else:
            st.warning("Could not load stats.")

    except requests.exceptions.ConnectionError:
        st.error("Stats unavailable.")

    except requests.exceptions.Timeout:
        st.error("Stats request timed out.")

    st.divider()

    st.header("📤 Upload Documents")

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    if st.button("🗑️ Reset Knowledge Base"):
        try:
            response = requests.delete(f"{BACKEND_URL}/reset", timeout=30)

            if response.status_code == 200:
                st.session_state.messages = []
                st.success(response.json().get("message", "Knowledge base reset."))
                st.rerun()
            else:
                st.error("Failed to reset knowledge base.")

        except requests.exceptions.ConnectionError:
            st.error("Backend is not running.")

        except requests.exceptions.Timeout:
            st.error("Reset request timed out.")

    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

    if uploaded_file is not None:
        with st.spinner("Processing PDF..."):
            try:
                files = {
                    "file": (uploaded_file.name, uploaded_file, "application/pdf")
                }

                response = requests.post(
                    f"{BACKEND_URL}/upload",
                    files=files,
                    timeout=120
                )

                if response.status_code == 200:
                    st.success(response.json().get("message", "PDF processed successfully."))
                else:
                    st.error("Failed to upload PDF.")

            except requests.exceptions.ConnectionError:
                st.error("Backend is not running. Start FastAPI first.")

            except requests.exceptions.Timeout:
                st.error("Upload request timed out. Try again.")

    st.divider()

    st.header("📄 Processed Documents")

    try:
        docs_response = requests.get(f"{BACKEND_URL}/documents", timeout=30)
        documents = docs_response.json().get("documents", [])

        if documents:
            for doc in documents:
                st.write(f"✅ {doc}")
        else:
            st.info("No documents uploaded yet.")

    except requests.exceptions.ConnectionError:
        st.error("Backend is not running.")

    except requests.exceptions.Timeout:
        st.error("Could not load documents.")


st.subheader("💬 Ask Questions")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

        if message.get("sources"):
            show_sources(message["sources"])


query = st.chat_input("Ask something from your uploaded documents...")

if query and not query.strip():
    st.warning("Please enter a valid question.")

if query and query.strip():
    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    with st.chat_message("user"):
        st.write(query)

    with st.chat_message("assistant"):
        with st.spinner("Searching documents and generating answer..."):
            try:
                chat_history = [
                    {
                        "role": msg["role"],
                        "content": msg["content"]
                    }
                    for msg in st.session_state.messages[-6:]
                ]

                response = requests.post(
                    f"{BACKEND_URL}/ask",
                    json={
                        "query": query,
                        "chat_history": chat_history
                    },
                    timeout=60
                )

                if response.status_code != 200:
                    st.error("Backend returned an error.")
                else:
                    data = response.json()

                    answer = data.get("answer", "No answer found.")
                    sources = data.get("sources", [])

                    st.write(answer)

                    if sources:
                        show_sources(sources)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })

            except requests.exceptions.ConnectionError:
                st.error("Backend is not running. Start FastAPI first.")

            except requests.exceptions.Timeout:
                st.error("Request timed out. Try again.")