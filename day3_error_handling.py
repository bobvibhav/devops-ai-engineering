'''import requests

try:
    response = requests.get("https://this-site-does-not-exist-12345.com")
    print(response.status_code)

except:
    print("Something went wrong with the request")
'''

import requests

try:
    response = requests.get("https://this-site-does-not-exist-12345.com")
    print(response.status_code)
except requests.exceptions.ConnectionError:
    print("Could not connect — check the URL or network")
except requests.exceptions.Timeout:
    print("The request took too long and timed out")
except Exception as e:
    print(f"Unexpected error: {e}")