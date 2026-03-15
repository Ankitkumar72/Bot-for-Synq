import os
import requests
import time
from flask import Flask
from threading import Thread

app = Flask('')

RENDER_URL = "https://bot-for-synq.onrender.com"
PING_INTERVAL = 600

@app.route('/')
def home():
    return "Bot is alive!"

def ping_bot():
    # Wait for the server to start
    time.sleep(5)
    while True:
        try:
            response = requests.get(RENDER_URL)
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Auto-Ping: {response.status_code}")
        except Exception as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Auto-Ping failed: {e}")
        time.sleep(PING_INTERVAL)

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    # Start the web server
    t1 = Thread(target=run)
    t1.daemon = True
    t1.start()
    
    # Start the pinger
    t2 = Thread(target=ping_bot)
    t2.daemon = True
    t2.start()
