import chromadb

documents = [
    "To connect to the VPN, open the company VPN client and enter your network credentials.",
    "To submit an expense report, log into the finance portal and upload your receipts.",
    "The office holiday calendar for this year is published on the HR intranet page.",
    "Password resets can be done through the self-service portal using your employee ID.",
]

client = chromadb.Client()
collection = client.create_collection(name="company_docs")
collection.add(documents=documents, ids=["doc1", "doc2", "doc3", "doc4"])

question = "How do I connect to the VPN?"
results = collection.query(query_texts=[question], n_results=2)

top_distance = results['distances'][0][0]
DISTANCE_THRESHOLD = 1.0

if top_distance > DISTANCE_THRESHOLD:
    print("I don't have information on that.")
else:
    import boto3
    import json

    retrieved_document = results['documents'][0][0]

    prompt = f"""Answer the question using only the context below.

    Context: {retrieved_document}

    Question: {question}
    """

    bedrock = boto3.client("bedrock-runtime", region_name="ap-south-1")

    body = json.dumps({
        "messages": [
            {"role": "user", "content": [{"text": prompt}]}
        ],
        "inferenceConfig": {"maxTokens": 100}
    })

    try:
        response = bedrock.invoke_model(
            modelId="apac.amazon.nova-micro-v1:0",
            body=body
        )
        result = json.loads(response["body"].read())
        answer = result['output']['message']['content'][0]['text']
        print(answer)
    except Exception as e:
        print(f"Something went wrong calling Bedrock: {e}")