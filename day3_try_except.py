import requests
def check_service_health(url):
    try:
        response = requests.get(url, timeout=5)
        return f"{url} is UP (status {response.status_code})"
    except requests.exceptions.ConnectionError:
        return f"{url} is DOWN — connection failed"
    except requests.exceptions.Timeout:
        return f"{url} is SLOW — timed out"
    except Exception as e:
        return f"{url} — unexpected error: {e}"
    
#print(check_service_health("https://api.github.com"))
#print(check_service_health("https://this-site-does-not-exist-12345.com"))


services = [
    "https://api.github.com",
    "https://this-site-does-not-exist-12345.com",
    "https://aws.amazon.com"
]
with open("health_check_log.txt", "a") as log_file:
    for service in services:
        result = check_service_health(service)
        print(result)
        log_file.write(result + "\n")




