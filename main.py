from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import datetime
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bot_state = {
    "status": "stopped",
    "balance": 0,
    "equity": 0,
    "spread": 0,
    "lot": 0,
    "h1_trend": "WAIT",
    "m5_trend": "WAIT",
    "float_pl": 0,
    "high_float": 0,
    "hold_hours": 0,
    "open_positions": 0,
    "strategy": "NONE",
    "signals": {
        "K03": "WAIT",
        "K08": "WAIT",
        "X05": "WAIT",
        "X08": "WAIT",
        "K05": "WAIT",
        "X03": "WAIT"
    },
    "active_strategies": 0,
    "last_update": "",
    "skip_reason": "Awaiting connection"
}

class CommandRequest(BaseModel):
    command: str
    params: dict = {}

@app.get("/")
def root():
    return {"status": "Liquidity X Bot API Running", "version": "2.0"}

@app.get("/status")
def get_status():
    return bot_state

@app.post("/command")
def send_command(cmd: CommandRequest):
    if cmd.command == "START":
        bot_state["status"] = "running"
        bot_state["last_update"] = str(datetime.datetime.now())
        return {"message": "Bot started", "status": "running"}
    elif cmd.command == "STOP":
        bot_state["status"] = "stopped"
        bot_state["last_update"] = str(datetime.datetime.now())
        return {"message": "Bot stopped", "status": "stopped"}
    elif cmd.command == "LOGIN":
        bot_state["last_update"] = str(datetime.datetime.now())
        return {"message": "Login processed", "status": "ok"}
    else:
        raise HTTPException(status_code=400, detail="Unknown command")

@app.post("/signal-update")
def update_signals(data: dict):
    for key in data:
        if key in bot_state and key != "signals":
            bot_state[key] = data[key]
        elif key == "signals":
            if isinstance(data[key], dict):
                for sig_key in data[key]:
                    if sig_key in bot_state["signals"]:
                        bot_state["signals"][sig_key] = data[key][sig_key]
    bot_state["last_update"] = str(datetime.datetime.now())
    return {"status": "updated"}

@app.get("/signals")
def get_signals():
    return bot_state["signals"]

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)