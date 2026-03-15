import time
import requests

# ⚠️ Replace this with your actual Render Web Service URL
# Example: "https://my-discord-bot-app.onrender.com"
RENDER_URL = "https://your-app-name.onrender.com"

# The interval to wait before pinging again 
# (10 minutes = 600 seconds. Render web services sleep after 15 minutes of inactivity)
PING_INTERVAL = 600 

def ping_bot():
    while True:
        try:
            response = requests.get(RENDER_URL)
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Pinged {RENDER_URL} - Status: {response.status_code}")
        except Exception as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Ping failed: {e}")
        
        time.sleep(PING_INTERVAL)

if __name__ == "__main__":
    print(f"Starting pinger. Will ping {RENDER_URL} every {PING_INTERVAL / 60} minutes...")
    ping_bot()
