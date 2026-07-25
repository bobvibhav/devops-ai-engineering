# RAG VPN Assistant

A small, complete **Retrieval-Augmented Generation (RAG)** pipeline built from scratch — retrieval, a confidence gate, and generation, wired end to end and running on **AWS Bedrock**.

Given a short knowledge base of company-style IT documents, this project answers natural-language questions grounded in that real data, and honestly declines to answer when nothing relevant is found — instead of letting the model guess.

## Why this project exists

Large Language Models generate fluent, confident-sounding text based on patterns learned during training — but they have no access to private or current data, and no built-in way to check whether their own output is true. RAG fixes this by retrieving the actual relevant documents first, then asking the model to generate an answer grounded in that real text, rather than relying purely on what it memorized.

## How it works

```
Documents  →  embedded and stored in a vector database (ChromaDB)      [done once]
Question   →  embedded with the same model                              [every query]
Vector DB  →  finds the closest-matching stored document(s)
Distance   →  checked against a threshold — too far means "I don't know"
Match      →  document + question sent to an LLM (AWS Bedrock — Amazon Nova Micro)
Answer     →  generated, grounded in the retrieved document
```

## Project structure

| File | Purpose |
|---|---|
| `rag_bedrock.py` | Main, current version — retrieval via ChromaDB, generation via AWS Bedrock |
| `rag_groq.py` | Earlier iteration — same retrieval logic, generation via Groq's free API |
| `requirements.txt` | Python dependencies |
| `.env.example` | Template for the `GROQ_API_KEY` needed only by `rag_groq.py` |

The project intentionally keeps both versions to show its own evolution: the retrieval half (ChromaDB, the confidence-gate distance check) is **identical** in both files — only the generation step and its API call differ. Swapping LLM providers required changing only a handful of lines, which is the point: RAG's core logic is provider-agnostic.

## Setup

```bash
pip install -r requirements.txt
```

**To run the Bedrock version** (`rag_bedrock.py`):
- Requires AWS credentials configured locally (`aws configure`) with Bedrock access in your region
- No `.env` file needed — authentication is handled via your AWS credentials

**To run the Groq version** (`rag_groq.py`):
- Copy `.env.example` to `.env` and add a real Groq API key from [console.groq.com](https://console.groq.com)

```bash
python rag_bedrock.py
```

## Example output

```
Q: How do I connect to the VPN?
A: To connect to the VPN, open the company VPN client and enter your network credentials.

Q: What's the weather today?
A: I don't have information on that.
```

The second question is correctly declined — its closest match in the knowledge base is too semantically distant to be a trustworthy answer, so the system says so instead of forcing a response from an irrelevant document.

## What this demonstrates

- Building a vector store and performing semantic retrieval with **ChromaDB**
- Using **similarity distance as a confidence signal**, not just returning the top match blindly
- Calling **AWS Bedrock** (`boto3`) for generation, including handling a real `ValidationException` around Bedrock's inference-profile requirement for certain models
- Keeping API keys out of source code entirely via `.env` / `python-dotenv` (Groq version)
- Structuring an LLM-calling pipeline with proper `try/except` error handling around the network call
- Swapping LLM providers with minimal code change, since RAG's retrieval and grounding logic is independent of which model generates the final answer

## Possible extensions

- Load documents from a real source (S3, a wiki export) instead of a hardcoded list
- Store the vector database persistently instead of in-memory per run
- Add a small CLI or simple web interface for asking questions interactively
