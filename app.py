import os

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

from chatbot import get_bot_reply
from database import init_db, save_message, get_history, clear_history

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv(
    "FLASK_SECRET_KEY",
    "local-development-only-change-this"
)

init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/history", methods=["GET"])
def history():
    return jsonify({"messages": get_history(limit=100)})


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()

    if not message:
        return jsonify({"error": "Please enter a message."}), 400

    if len(message) > 4000:
        return jsonify({"error": "Message is too long."}), 400

    save_message("user", message)

    try:
        reply = get_bot_reply(message, get_history(limit=12))
    except Exception:
        app.logger.exception("AI response failed")
        reply = (
            "Sorry, I could not generate a response. "
            "Check your AI API configuration and try again."
        )

    save_message("assistant", reply)

    return jsonify({"reply": reply})


@app.route("/api/clear", methods=["POST"])
def clear():
    clear_history()
    return jsonify({"success": True})


if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug_mode)