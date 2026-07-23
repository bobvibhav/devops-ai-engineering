documents = [
    "To connect to the VPN, open the company VPN client and enter your network credentials.",
    "To submit an expense report, log into the finance portal and upload your receipts.",
    "The office holiday calendar for this year is published on the HR intranet page.",
    "Password resets can be done through the self-service portal using your employee ID.",
]

import chromadb
client = chromadb.Client()
collection = client.create_collection(name="company_docs")
collection.add(
    documents=documents,
    ids=["doc1", "doc2", "doc3", "doc4"]
)

results = collection.query(
    query_texts=["How do I connect to the VPN?"],
    n_results=2
)

#print(results)

top_distance = results['distances'][0][0]
DISTANCE_THRESHOLD = 1.0
if top_distance > DISTANCE_THRESHOLD:
    print("I don't have information on that.")
else:

    from dotenv import load_dotenv
    import os, requests

    load_dotenv()
    groq_api_key = os.getenv("GROQ_API_KEY")

    retrieved_document = results['documents'][0][0]
    question = "How do I connect to the VPN?"

    prompt = f"""Answer the question using only the context below.

    Context: {retrieved_document}

    Question: {question}
    """

    try:
        response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {groq_api_key}"},
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": prompt}]
        },
        timeout=10
    )
#    print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Something went wrong calling the LLM: {e}")

    answer = response.json()['choices'][0]['message']['content']
    print(answer)