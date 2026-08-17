from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # <-- THIS FIXES "Awaiting connection"

# This is what your frontend will read
live_data = {
    "balance": 0.00,
    "equity": 0.00,
    "spread": 0.00,
    "lot": 0.00,
    "h1_trend": "WAIT",
    "m5_trend": "WAIT",
    "pnl": 0.00,
    "positions": "0 / 6",
    "signals": {
        "K03": "WAIT", "K08": "WAIT", "X05": "WAIT",
        "X08": "WAIT", "K05": "WAIT", "X03": "WAIT"
    },
    "status": "running"
}

@app.route('/')
def home():
    return jsonify({"status":"Liquidity X Bot API Running","version":"2.0"})

@app.route('/api/status')
def status():
    # HERE you put your real Deriv/MT5 logic to update live_data
    return jsonify(live_data)

@app.route('/api/start')
def start():
    live_data["status"] = "running"
    return jsonify({"msg": "Bot started"})

@app.route('/api/stop')
def stop():
    live_data["status"] = "stopped"
    return jsonify({"msg": "Bot stopped"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
