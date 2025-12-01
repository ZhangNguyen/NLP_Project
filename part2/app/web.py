from flask import Flask, render_template, request, jsonify
from .chatbot import FoodChatbot

app = Flask(__name__, template_folder="templates")

# Tạo một instance chatbot dùng chung cho cả web app
bot = FoodChatbot()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "empty message"}), 400

    try:
        reply = bot.handle(message)
    except Exception as e:
        reply = f"Xin lỗi, hệ thống gặp lỗi: {e}"

    return jsonify({"reply": reply})


def create_app():
    return app


if __name__ == "__main__":
    # Chạy dev mode (ngoài Docker)
    app.run(host="0.0.0.0", port=8000, debug=True)
