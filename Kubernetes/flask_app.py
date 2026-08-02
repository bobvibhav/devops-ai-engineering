from flask import Flask
import socket

app = Flask(__name__)

@app.route("/")
def home():
    hostname = socket.gethostname()
    return f"Hello from Pod: {hostname}\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)