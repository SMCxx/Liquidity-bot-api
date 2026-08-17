from flask import Flask, jsonify, render_template_string
from flask_cors import CORS
import os, random, time, threading

app = Flask(__name__)
CORS(app)

# ---- THIS IS YOUR LIVE BOT DATA ----
# Later you will replace this with real Deriv API calls
live_data = {
    "balance": 124.50,
    "equity": 124.50,
    "spread": 0.7,
    "lot": 0.10,
    "h1_trend": "BULLISH",
    "m5_trend": "BULLISH",
    "pnl": 0.00,
    "positions": "0 / 6",
    "signals": {"K03": "BUY", "K08": "WAIT", "X05": "BUY", "X08": "WAIT", "K05": "WAIT", "X03": "WAIT"},
    "status": "running"
}

def bot_loop():
    # Simulate live market - replace with your real Liquidity X logic
    while True:
        live_data["spread"] = round(random.uniform(0.5, 1.2), 2)
        live_data["balance"] = round(live_data["balance"] + random.uniform(-0.1, 0.2), 2)
        live_data["equity"] = live_data["balance"]
        time.sleep(3)

# ---- FRONTEND UI (your controller) ----
HTML = """
<!DOCTYPE html>
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{background:#0e0e0e;color:white;font-family:sans-serif;padding:15px}
.card{background:#1a1a1a;border-radius:12px;padding:15px;margin-bottom:12px}
.green{color:#00ff88}
</style></head><body>
<h2>💰 Liquidity X<br><small>Bot Controller</small></h2>
<div class="card">
<div>Balance <span id="bal" style="float:right">$0.00</span></div>
<div>Equity <span id="eq" style="float:right">$0.00</span></div>
<div>Spread <span id="spr" style="float:right">0.00</span></div>
<div>Lot <span id="lot" style="float:right">0.00</span></div>
</div>
<div class="card">
<div>H1 Trend <span id="h1" style="float:right">WAIT</span></div>
<div>M5 Trend <span id="m5" style="float:right">WAIT</span></div>
<div>P&L <span id="pnl" class="green" style="float:right">$0.00</span></div>
<div>Positions <span id="pos" style="float:right">0 / 6</span></div>
</div>
<div class="card">
<div>Signals</div>
<div>K03 <span id="k03" style="float:right">WAIT</span></div>
<div>K08 <span id="k08" style="float:right">WAIT</span></div>
<div>X05 <span id="x05" style="float:right">WAIT</span></div>
</div>
<script>
async function update(){
  try{
    const res = await fetch('/api/status');
    const d = await res.json();
    document.getElementById('bal').innerText = '$'+d.balance;
    document.getElementById('eq').innerText = '$'+d.equity;
    document.getElementById('spr').innerText = d.spread;
    document.getElementById('lot').innerText = d.lot;
    document.getElementById('h1').innerText = d.h1_trend;
    document.getElementById('m5').innerText = d.m5_trend;
    document.getElementById('pnl').innerText = '$'+d.pnl;
    document.getElementById('pos').innerText = d.positions;
    document.getElementById('k03').innerText = d.signals.K03;
    document.getElementById('k08').innerText = d.signals.K08;
    document.getElementById('x05').innerText = d.signals.X05;
  }catch(e){}
}
setInterval(update, 3000);
update();
</script></body></html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/api/status')
def status():
    return jsonify(live_data)

if __name__ == "__main__":
    threading.Thread(target=bot_loop, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
