"""
CineBot - Flask backend (Lex verzija).
Pokretanje: python app.py
Otvori u browseru: http://localhost:5000
"""

import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

import lex_client
import conversation

load_dotenv()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Please type something.", "debug": {}})

    # 1. Posalji Lex-u
    parsed = lex_client.parse_message(user_message)

    # 2. Generiraj odgovor (proslijedjujemo i originalni tekst za gibberish detekciju)
    reply = conversation.respond(parsed, user_text=user_message)

    # 3. Debug info
    debug = {
        "intent": parsed.get("intent"),
        "confidence": round(parsed.get("intent_confidence", 0.0), 2),
        "entities": parsed.get("entities", {}),
        "dialog_state": parsed.get("dialog_state"),
    }

    return jsonify({"reply": reply, "debug": debug})


@app.route("/reset", methods=["POST"])
def reset():
    conversation.reset_context()
    lex_client.reset_session()
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    print("=" * 60)
    print("🎬 CineBot is starting...")
    print("Open http://localhost:5000 in your browser")
    print(f"Lex Bot ID: {os.getenv('LEX_BOT_ID')}")
    print(f"Region: {os.getenv('AWS_REGION')}")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=debug)
