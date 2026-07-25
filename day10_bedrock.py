import boto3
import json

bedrock = boto3.client("bedrock-runtime", region_name="ap-south-1")

body = json.dumps({
    "messages": [
        {"role": "user", "content": [{"text": "Say hello in one short sentence."}]}
    ],
    "inferenceConfig": {"maxTokens": 50}
})

response = bedrock.invoke_model(
    modelId="apac.amazon.nova-micro-v1:0",
    body=body
)

result = json.loads(response["body"].read())
#print(result)
answer = result['output']['message']['content'][0]['text']
print(answer)