import requests
from datetime import datetime

response = requests.get("https://api.github.com")

log_line = f"{datetime.now()} - GitHub API status: {response.status_code}\n"

with open("/app/data/api_log.txt", "a") as f:
    f.write(log_line)

print(log_line)