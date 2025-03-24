from flask import Flask
import requests

app = Flask(__name__)

@app.route("/")
def pipedrive_sync():
    # Šeit paliek tava Pipedrive loģika
    # Dummy piemērs:
    return "Pipedrive test service running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
