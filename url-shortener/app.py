import string
import random
import socket
import requests
from flask import Flask, request, jsonify, redirect

app = Flask(__name__)

# In-memory storage for URLs
url_mapping = {}

# === 🔐 SPLUNK CONFIG ===
SPLUNK_HEC_URL = "http://192.168.100.12:8088/services/collector/event"
SPLUNK_TOKEN = "e7b56751-7dbb-41a5-a6a4-87233331a0c2"
SPLUNK_HEADERS = {
    "Authorization": f"Splunk {SPLUNK_TOKEN}"
}

def log_to_splunk(event):
    try:
        payload = {
            "event": event,
            "sourcetype": "url-shortener"
        }
        res = requests.post(SPLUNK_HEC_URL, headers=SPLUNK_HEADERS, json=payload, timeout=2)
        print("✅ Splunk log sent:", res.status_code)
    except Exception as e:
        print("❌ Error sending to Splunk:", e)

# === 🔗 ROUTES ===

@app.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()
    original_url = data.get("url")

    if not original_url:
        return jsonify({"error": "Missing URL"}), 400

    short_id = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    short_url = f"http://url.local:30080/{short_id}"

    url_mapping[short_id] = original_url

    # Log to Splunk
    log_to_splunk({
        "short_id": short_id,
        "short_url": short_url,
        "original_url": original_url,
        "client_ip": request.remote_addr,
        "host": socket.gethostname()
    })

    return jsonify({"short_url": short_url})

@app.route("/<short_id>")
def redirect_url(short_id):
    original_url = url_mapping.get(short_id)
    if original_url:
        return redirect(original_url)
    return jsonify({"error": "Not found"}), 404

@app.route("/health")
def health_check():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
