"""
RAG VPN Assistant — Groq edition (earlier iteration)
------------------------------------------------------
This was the first working version of this pipeline, using Groq's free LLM
API for the generation step before the project was migrated to AWS Bedrock
(see rag_bedrock.py). Kept here to show the project's evolution: the
retrieval half (ChromaDB, the confidence-gate distance check) is identical
in both versions — only the generation step and its API call differ.

Requires a GROQ_API_KEY in a local .env file (see .env.example).
"""

import os
import requests
import chromadb
from dotenv import load_dotenv

DOCUMENTS = [
    "To connect to the VPN, open the company VPN client and enter your network credentials.",
    "To submit an expense report, log into the finance portal and upload your receipts.",
    "The office holiday calendar for this year is published on the HR intranet page.",
    "Password resets can be done through the self-service portal using your employee ID.",
]
DOCUMENT_IDS = ["doc1", "doc2", "doc3", "doc4"]
DISTANCE_THRESHOLD = 1.0
GROQ_MODEL = "llama-3.1-8b-instant"


def build_knowledge_base():
    client = chromadb.Client()
    collection = client.create_collection(name="company_docs")
    collection.add(documents=DOCUMENTS, ids=DOCUMENT_IDS)
    return collection


def build_prompt(retrieved_document, question):
    return f"""Answer the question using only the context below.

Context: {retrieved_document}

Question: {question}
"""


def call_groq(prompt, api_key):
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": GROQ_MODEL,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=10,
    )
    return response.json()["choices"][0]["message"]["content"]


def answer_question(collection, question, api_key):
    results = collection.query(query_texts=[question], n_results=2)
    top_distance = results["distances"][0][0]

    if top_distance > DISTANCE_THRESHOLD:
        return "I don't have information on that."

    retrieved_document = results["documents"][0][0]
    prompt = build_prompt(retrieved_document, question)

    try:
        return call_groq(prompt, api_key)
    except requests.exceptions.RequestException as e:
        return f"Something went wrong calling the LLM: {e}"


if __name__ == "__main__":
    load_dotenv()
    groq_api_key = os.getenv("GROQ_API_KEY")

    kb = build_knowledge_base()

    for q in ["How do I connect to the VPN?", "What's the weather today?"]:
        print(f"Q: {q}")
        print(f"A: {answer_question(kb, q, groq_api_key)}")
        print()
