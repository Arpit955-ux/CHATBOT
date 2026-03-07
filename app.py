import os
import random
import re
from threading import Lock
from typing import Dict, List, Optional

import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

RASA_URL = os.getenv("RASA_URL", "http://localhost:5005/webhooks/rest/webhook")
DEFAULT_SENDER = os.getenv("DEFAULT_SENDER", "web-user")
RASA_TIMEOUT_SECONDS = int(os.getenv("RASA_TIMEOUT_SECONDS", "8"))
FORCE_LOCAL_NLP = os.getenv("FORCE_LOCAL_NLP", "0").strip().lower() in {"1", "true", "yes"}

SESSION_STATE: Dict[str, Dict[str, Optional[str]]] = {}
SESSION_LOCK = Lock()

QUOTE_BANK = {
    "inspiration": [
        "Believe you can, and you're halfway there. - Theodore Roosevelt",
        "Act as if what you do makes a difference. It does. - William James",
        "Keep your face always toward the sunshine, and shadows will fall behind you. - Walt Whitman",
    ],
    "motivation": [
        "Do something today that your future self will thank you for.",
        "Success is the sum of small efforts, repeated day in and day out. - Robert Collier",
        "Great things never come from comfort zones.",
    ],
    "success": [
        "Success usually comes to those who are too busy to be looking for it. - Henry David Thoreau",
        "The road to success and the road to failure are almost exactly the same. - Colin R. Davis",
        "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
    ],
    "love": [
        "Love recognizes no barriers. - Maya Angelou",
        "Where there is love there is life. - Mahatma Gandhi",
        "To love and be loved is to feel the sun from both sides. - David Viscott",
    ],
    "funny": [
        "I'm not arguing, I'm just explaining why I'm right.",
        "People say nothing is impossible, but I do nothing every day. - A. A. Milne",
        "My bed is a magical place where I suddenly remember everything I forgot to do.",
    ],
}

INTENT_KEYWORDS = {
    "greet": {"hi", "hello", "hey", "good morning", "good evening", "namaste"},
    "goodbye": {"bye", "goodbye", "see you", "good night", "take care"},
    "thanks": {"thanks", "thank you", "thx", "appreciate", "your welcome", "you're welcome"},
    "satisfied": {"yes", "yep", "yeah", "good", "nice", "helpful", "liked it"},
    "not_satisfied": {"no", "nope", "not helpful", "bad", "another", "not good"},
    "bot_challenge": {"are you a bot", "are you human", "who are you", "what are you"},
    "inspiration": {"inspiration", "inspirational", "inspire", "uplift", "uplifting"},
    "motivation": {"motivation", "motivational", "motivate", "push me", "encourage me"},
    "success": {"success", "achieve", "goal", "win", "winning"},
    "love": {"love", "romantic", "relationship", "heart"},
    "funny": {"funny", "humor", "humour", "joke", "laugh"},
}


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def _contains(text: str, options: set) -> bool:
    return any(option in text for option in options)


def _detect_intent(message: str) -> str:
    text = _normalize(message)

    for intent in [
        "bot_challenge",
        "goodbye",
        "thanks",
        "satisfied",
        "not_satisfied",
        "inspiration",
        "motivation",
        "success",
        "love",
        "funny",
        "greet",
    ]:
        if _contains(text, INTENT_KEYWORDS[intent]):
            return intent

    return "unknown"


def _get_session(sender: str) -> Dict[str, Optional[str]]:
    with SESSION_LOCK:
        if sender not in SESSION_STATE:
            SESSION_STATE[sender] = {
                "awaiting_feedback": "0",
                "last_category": None,
            }
        return SESSION_STATE[sender]


def _quote_response(category: str, sender: str) -> List[str]:
    quote = random.choice(QUOTE_BANK[category])
    session = _get_session(sender)
    session["awaiting_feedback"] = "1"
    session["last_category"] = category
    category_name = {
        "inspiration": "inspirational",
        "motivation": "motivational",
        "success": "success",
        "love": "love",
        "funny": "funny",
    }[category]

    return [
        f"Here's a {category_name} quote for you:",
        quote,
        "Is this quote helpful to you? Type 'yes' or 'no'.",
    ]


def query_local_nlp(message: str, sender: str) -> List[str]:
    intent = _detect_intent(message)
    session = _get_session(sender)

    if intent == "greet":
        return [
            "Hey hi, please tell me which quotes you want today (Inspirational/Motivational/Success/Love/Funny)."
        ]

    if intent in {"inspiration", "motivation", "success", "love", "funny"}:
        return _quote_response(intent, sender)

    awaiting_feedback = session.get("awaiting_feedback") == "1"

    if intent == "satisfied" and awaiting_feedback:
        session["awaiting_feedback"] = "0"
        return ["Thanks for your feedback. If you want more quotes, mention the quote type."]

    if intent == "not_satisfied" and awaiting_feedback:
        session["awaiting_feedback"] = "0"
        return [
            "No issue. Tell me another category: Inspirational, Motivational, Success, Love, or Funny."
        ]

    if intent == "thanks":
        return ["You're welcome."]

    if intent == "goodbye":
        session["awaiting_feedback"] = "0"
        return ["Bye. Stay positive and have a great day."]

    if intent == "bot_challenge":
        return ["I am a Quotes Recommendation Bot powered by NLP."]

    return [
        "I can help with quotes. Please type one category: Inspirational, Motivational, Success, Love, or Funny."
    ]


def query_rasa(message: str, sender: str) -> List[str]:
    payload = {"sender": sender, "message": message}

    try:
        response = requests.post(RASA_URL, json=payload, timeout=RASA_TIMEOUT_SECONDS)
        response.raise_for_status()
    except requests.RequestException:
        return []

    bot_messages = response.json()
    replies: List[str] = []

    for item in bot_messages:
        text = str(item.get("text", "")).strip()
        if text:
            replies.append(text)

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

    source = "local"

    if not FORCE_LOCAL_NLP:
        rasa_replies = query_rasa(message=message, sender=sender)
        if rasa_replies:
            return jsonify({"replies": rasa_replies, "mode": "rasa"})

    local_replies = query_local_nlp(message=message, sender=sender)
    return jsonify({"replies": local_replies, "mode": source})


if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
