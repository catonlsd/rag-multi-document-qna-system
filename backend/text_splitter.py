from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_chunks(pages, filename):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=250,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = []

    for page in pages:
        page_text = page["text"].strip()

        if not page_text:
            continue

        page_chunks = text_splitter.split_text(page_text)

        for i, chunk in enumerate(page_chunks):
            chunks.append({
                "content": chunk,
                "metadata": {
                    "source": filename,
                    "page": page["page_number"],
                    "chunk_id": f"{filename}_page_{page['page_number']}_chunk_{i + 1}"
                }
            })

    return chunks