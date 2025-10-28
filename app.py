from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

GROQ_API_KEY = "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"
API_URL = "https://api.groq.com/openai/v1/chat/completions"


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip()

    # 🔹 Əgər istifadəçi mesaj göndərməyibsə
    if not user_message:
        return jsonify({"reply": "Zəhmət olmasa bir mesaj yazın 😊"}), 400

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # 🧠 Shopping Chat üçün system mesajı
    system_message = (
        "Sən 'Shopping Chat' adında mehriban və peşəkar alış-veriş köməkçisisən. "
        "İstifadəçiyə məhsullar, qiymətlər, endirimlər və moda trendləri barədə məlumat ver. "
        "Cavablarını qısa, maraqlı və müsbət tonda yaz. "
        "Əgər sual konkret məhsulla bağlı deyilsə, yenə də alış-verişlə əlaqələndirməyə çalış."
    )

    chat_data = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
    }

    # 🔸 Groq API-yə sorğu
    chat_response = requests.post(API_URL, headers=headers, json=chat_data)
    chat_result = chat_response.json()

    # 🧾 Xəta yoxlaması
    if "choices" not in chat_result:
        print("⚠️ API Error:", chat_result)
        error_msg = chat_result.get("error", {}).get("message", "Naməlum xəta baş verdi.")
        return jsonify({"reply": f"Bağışla, serverdə problem yarandı: {error_msg}"}), 500

    ai_reply = chat_result["choices"][0]["message"]["content"]

    return jsonify({
        "name": "Shopping Chat",
        "reply": ai_reply
    })


@app.route("/messages", methods=["GET"])
def get_messages():
    """messages.json faylını oxuyub qaytarır"""
    try:
        with open("messages.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "messages.json tapılmadı."}), 404


if __name__ == "__main__":
    print("🛍️ Shopping Chat server işə salındı: http://127.0.0.1:5000")
    app.run(debug=True)
