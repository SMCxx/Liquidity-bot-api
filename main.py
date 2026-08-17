from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

live_data = {
  "balance":0,"equity":0,"spread":0,"lot":0,"h1_trend":"WAIT","m5_trend":"WAIT",
  "pnl":0,"positions":"0 / 6","signals":{"K03":"WAIT","K08":"WAIT","X05":"WAIT","X08":"WAIT","K05":"WAIT","X03":"WAIT"},
  "skip":"Awaiting MT5...","status":"offline","last_update":"never"
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/status')
def status():
    return jsonify(live_data)

@app.route('/api/update', methods=['POST'])
def update():
    global live_data
    data = request.get_json(force=True)
    data["last_update"] = datetime.utcnow().strftime("%H:%M:%S UTC")
    data["status"] = "running"
    live_data = data
    return jsonify({"ok":True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
