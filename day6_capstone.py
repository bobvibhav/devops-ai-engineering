
'''Question: Design a class ServiceMonitor
Write a Python program to design a class ServiceMonitor that checks the health of multiple web services and keeps a record of the results.
(a) The class should have the following attributes, set in __init__:

services — a list of URLs to monitor (passed in when the object is created)
results — an empty list, used to store the outcome of each check

(b) Implement the following methods:

check_one(self, url) — attempts to reach the given url using requests.get(), with a timeout. It should:

Return "UP" if the request succeeds (status code 200)
Return "DOWN" if a ConnectionError or Timeout occurs
Never let the program crash, regardless of what goes wrong


check_all(self) — loops through every URL in self.services, calls check_one() on each, and appends a result (e.g. a dict like {"url": ..., "status": ...}) to self.results
show_results(self) — prints every entry currently stored in self.results, in a readable format

(c) Store the list of URLs to monitor inside a .env file (not hardcoded in the script), and load it using python-dotenv — reusing Day 4's config pattern.
(d) Create one ServiceMonitor object, call check_all(), then call show_results(), and confirm the output correctly shows a mix of UP and DOWN services.
'''
import requests
from dotenv import load_dotenv
import os
class ServiceMonitor:
    

    def __init__(self, services):
        self.services = services
        self.results = []

    def check_one(self, url):

        try:
            response= requests.get(url, timeout=5)
            return f" UP and status code is {response.status_code}"
        except requests.exceptions.ConnectionError:
            return f"DOWN - connectionError"
        except requests.exceptions.Timeout:
            return f" DOWN"
        except Exception as e:
            return f"unexpected error: {e}"
        
    def check_all(self):
        for url in self.services:
            result= self.check_one(url)
            self.results.append({"url": url, "status": result})

    def show_results(self):
        for site in self.results:
            print(f"{site['url']} → {site['status']}")
load_dotenv()
services_string = os.getenv("SERVICES")
services_list = services_string.split(",")

monitor = ServiceMonitor(services_list)
monitor.check_all()
monitor.show_results()