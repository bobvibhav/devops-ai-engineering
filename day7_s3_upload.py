import boto3

s3 = boto3.client("s3")
s3.upload_file("github_data.json", "vibhav-private-bucket-123", "embeddings/github_data.json")
print("Upload complete")

response = s3.list_objects_v2(Bucket="vibhav-private-bucket-123")
for obj in response['Contents']:
    print(obj['Key'])