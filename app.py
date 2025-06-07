from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

OANDA_API_KEY = os.getenv("OANDA_API_KEY")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")

@app.route('/')
def home():
    return "Auto FX Flask 서버 작동 중"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("📩 Webhook 수신:", data)

    if data.get("signal") == "BUY":
        price = float(data["price"])
        entry = round(price - 0.0003, 5)
        tp = round(price + 0.0015, 5)
        sl = round(price - 0.0010, 5)

        order = {
            "order": {
                "units": "1000",
                "instrument": data["pair"],
                "type": "LIMIT",
                "positionFill": "DEFAULT",
                "price": str(entry),
                "takeProfitOnFill": {"price": str(tp)},
                "stopLossOnFill": {"price": str(sl)}
            }
        }

        headers = {
            "Authorization": f"Bearer {OANDA_API_KEY}",
            "Content-Type": "application/json"
        }

        url = f"https://api-fxpractice.oanda.com/v3/accounts/{ACCOUNT_ID}/orders"
        r = requests.post(url, headers=headers, data=json.dumps(order))
        print("📤 주문 응답:", r.status_code, r.text)
        return {"status": "order sent", "response": r.json()}

    return {"status": "ignored"}
    if __name__ == "__main__":
        port = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", port=port)
