"""
RAG VPN Assistant
------------------
A small, complete Retrieval-Augmented Generation (RAG) pipeline.

Given a short knowledge base of company-style documents, this script:
  1. Stores each document as an embedding in a local ChromaDB vector store.
  2. Embeds an incoming question and retrieves the closest-matching document(s).
  3. Checks a similarity-distance threshold before trusting the match — if
     nothing relevant is found, it says so instead of guessing.
  4. Sends the retrieved document + question to AWS Bedrock (Amazon Nova
     Micro) to generate a grounded, natural-language answer.

Author: Vibhav Mishra
"""

import json
import boto3
import chromadb

# --------------------------------------------------------------------------
# 1. Knowledge base (in a real system, this would be pulled from a wiki,
#    Confluence, S3, etc. Kept small and hardcoded here for a clear demo.)
# --------------------------------------------------------------------------
DOCUMENTS = [
    "To connect to the VPN, open the company VPN client and enter your network credentials.",
    "To submit an expense report, log into the finance portal and upload your receipts.",
    "The office holiday calendar for this year is published on the HR intranet page.",
    "Password resets can be done through the self-service portal using your employee ID.",
]
DOCUMENT_IDS = ["doc1", "doc2", "doc3", "doc4"]

# A result whose closest match is farther than this distance is treated as
# "no relevant information found" rather than forced into an answer.
DISTANCE_THRESHOLD = 1.0

# AWS Bedrock inference profile ID for the model being used.
BEDROCK_MODEL_ID = "apac.amazon.nova-micro-v1:0"
BEDROCK_REGION = "ap-south-1"


def build_knowledge_base():
    """Create an in-memory ChromaDB collection and load the documents into it."""
    client = chromadb.Client()
    collection = client.create_collection(name="company_docs")
    collection.add(documents=DOCUMENTS, ids=DOCUMENT_IDS)
    return collection


def retrieve(collection, question, n_results=2):
    """Embed the question and return the closest matching stored documents."""
    return collection.query(query_texts=[question], n_results=n_results)


def build_prompt(retrieved_document, question):
    """Combine the retrieved context and the question into one grounded prompt."""
    return f"""Answer the question using only the context below.

Context: {retrieved_document}

Question: {question}
"""


def call_bedrock(prompt):
    """Send the prompt to AWS Bedrock and return the generated answer text."""
    bedrock = boto3.client("bedrock-runtime", region_name=BEDROCK_REGION)

    body = json.dumps({
        "messages": [
            {"role": "user", "content": [{"text": prompt}]}
        ],
        "inferenceConfig": {"maxTokens": 150},
    })

    response = bedrock.invoke_model(modelId=BEDROCK_MODEL_ID, body=body)
    result = json.loads(response["body"].read())
    return result["output"]["message"]["content"][0]["text"]


def answer_question(collection, question):
    """Full RAG flow for a single question: retrieve, gate, generate."""
    results = retrieve(collection, question)
    top_distance = results["distances"][0][0]

    if top_distance > DISTANCE_THRESHOLD:
        return "I don't have information on that."

    retrieved_document = results["documents"][0][0]
    prompt = build_prompt(retrieved_document, question)

    try:
        return call_bedrock(prompt)
    except Exception as e:
        return f"Something went wrong calling Bedrock: {e}"


if __name__ == "__main__":
    kb = build_knowledge_base()

    test_questions = [
        "How do I connect to the VPN?",
        "What's the weather today?",
    ]

    for q in test_questions:
        print(f"Q: {q}")
        print(f"A: {answer_question(kb, q)}")
        print()
