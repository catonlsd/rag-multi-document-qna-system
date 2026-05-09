import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def build_prompt(question, relevant_chunks, chat_history=None):
    context = "\n\n".join([
        f"Source: {chunk['metadata']['source']} | Page: {chunk['metadata']['page']}\n{chunk['content']}"
        for chunk in relevant_chunks
    ])

    history_text = ""

    if chat_history:
        for msg in chat_history:
            history_text += f"{msg['role'].upper()}: {msg['content']}\n"

    return f"""
You are a helpful AI assistant for a Multi-Document QnA system.

Strict Rules:
1. Answer ONLY from the provided document context.
2. Do NOT infer, assume, or add outside knowledge.
3. If the answer is incomplete in the documents, clearly say so.
4. Keep answers concise and factual.

Conversation History:
{history_text}

Document Context:
{context}

Question:
{question}

Answer:
"""


def generate_answer(question, relevant_chunks, chat_history=None):
    prompt = build_prompt(question, relevant_chunks, chat_history)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


def stream_answer(question, relevant_chunks, chat_history=None):
    prompt = build_prompt(question, relevant_chunks, chat_history)

    stream = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        stream=True
    )

    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            yield content