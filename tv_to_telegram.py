
from flask import Flask, request
import requests
import json

app = Flask(__name__)

TELEGRAM_TOKEN = "6925170785:AAGgnMoPoJ5JEO6UKK1GJKduOvVL9oYaxRE"
CHAT_ID = "6387016096"

@app.route("/", methods=["POST"])
def webhook():
    try:
        data = request.data.decode("utf-8")
        payload = json.loads(data) if data.startswith("{") else {}

        entry_price = float(payload.get("entry_price", 30000))
        leverage = int(payload.get("leverage", 10))
        position_usdt = float(payload.get("position_usdt", 3000))

        sl1 = round(entry_price * 0.99, 2)
        sl2 = round(entry_price * 0.98, 2)
        liq = round(entry_price * (1 - 1 / leverage), 2)

        message = f"""🚀 [롱 진입 시그널 발생]

📌 전략명: ETHUSDT 2H 롱전용 EMA 전략
🥇 진입가: {entry_price:,} USDT
📈 레버리지: {leverage}배
📦 진입 비중: {position_usdt:,.0f} USDT (총 시드의 {int(position_usdt / 10000 * 100)}%)

❌ 손절가 -1%: {sl1:,} USDT
❌ 손절가 -2%: {sl2:,} USDT
🚨 강제청산가: {liq:,} USDT
"""
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", data={
            "chat_id": CHAT_ID,
            "text": message
        })
        return "sent"
    except Exception as e:
        return f"error: {e}"
