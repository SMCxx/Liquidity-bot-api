from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import os, threading, time, json, websocket

app = Flask(__name__)
CORS(app)

live_data = {
    "balance": 0.00, "equity": 0.00, "spread": 0.00, "lot": 0.00,
    "h1_trend": "WAIT", "m5_trend": "WAIT", "pnl": 0.00,
    "positions": "0 / 6",
    "signals": {"K03": "WAIT", "K08": "WAIT", "X05": "WAIT", "X08": "WAIT", "K05": "WAIT", "X03": "WAIT"},
    "status": "Awaiting connection"
}

def get_deriv_balance():
    # REAL LIVE DATA from Deriv
    try:
        token = os.getenv("DERIV_TOKEN")  # Set this in Render > Environment
        if not token:
            print("No DERIV_TOKEN set")
            return
        
        ws = websocket.create_connection("wss://ws.derivws.com/websockets/v3?app_id=1089")
        ws.send(json.dumps({"authorize": token}))
        auth = json.loads(ws.recv())
        
        if "error" in auth:
            print(auth["error"])
            return

        ws.send(json.dumps({"balance": 1}))
        bal_res = json.loads(ws.recv())
        balance = bal_res["balance"]["balance"]
        
        live_data["balance"] = balance
        live_data["equity"] = balance
        live_data["status"] = "running"
        print(f"Live Balance: {balance}")
        ws.close()
    except Exception as e:
        print(f"Deriv Error: {e}")
        live_data["status"] = "Awaiting connection"

def bot_loop():
    while True:
        get_deriv_balance()
        # HERE put your real K03/X05/H1 Trend logic
        # For now it will just update balance every 10 sec
        time.sleep(10)

@app.route('/')
def home():
    return render_template('index.html') # serves your real UI

@app.route('/api/status')
def api_status():
    return jsonify(live_data)

if __name__ == "__main__":
    threading.Thread(target=bot_loop, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
