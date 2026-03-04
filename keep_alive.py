from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    # Run the Flask app on port 8080 (or whatever hosting platform assigns)
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    # Create a background thread so it doesn't block the Discord bot
    t = Thread(target=run)
    t.start()
