import os
from typing import List

import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

RASA_URL = os.getenv("RASA_URL", "http://localhost:5005/webhooks/rest/webhook")
DEFAULT_SENDER = os.getenv("DEFAULT_SENDER", "web-user")


def query_rasa(message: str, sender: str) -> List[str]:
    payload = {"sender": sender, "message": message}
    try:
        response = requests.post(RASA_URL, json=payload, timeout=20)
        response.raise_for_status()
    except requests.RequestException:
        return ["I am unable to reach the chatbot server right now. Please try again in a moment."]

    bot_messages = response.json()
    replies: List[str] = []

    for item in bot_messages:
        if item.get("text"):
            replies.append(item["text"])

    if not replies:
        replies.append("I did not understand that. Try asking for motivational, inspirational, love, funny, or success quotes.")

    return replies


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    sender = str(data.get("sender", DEFAULT_SENDER)).strip() or DEFAULT_SENDER

    if not message:
        return jsonify({"error": "Message cannot be empty."}), 400

    replies = query_rasa(message=message, sender=sender)
    return jsonify({"replies": replies})


if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
