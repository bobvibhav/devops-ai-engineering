import requests
import json

response = requests.get("https://api.github.com")

print (response.status_code)

data = response.json()
print(data['current_user_url'])

with open("github_data.json", "w") as file:
    json.dump(data, file, indent=2)