from flask import Flask, request
import requests
import os

app = Flask(__name__)  # ✅ 한 번만 선언

# 텔레그램 설정
bot_token = "여기에_봇토큰_입력"
chat_id = "여기에_챗ID_입력"

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    message = data.get("message", "📢 새로운 시그널 발생!")

    # 텔레그램 메시지 전송
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, json=payload)
        return "OK", response.status_code
    except Exception as e:
        return str(e), 500

# Render 환경용 포트 설정
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# ✅ gunicorn용 엔트리포인트
gunicorn_app = app
