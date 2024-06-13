import os
import logging
from pyrogram.raw.all import layer
from pyrogram import Client, idle, __version__

from config import Config
from flask import Flask, request
import threading

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Handle webhook
    return "OK"

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Ensure download directory exists
if not os.path.isdir(Config.DOWNLOAD_LOCATION):
    os.makedirs(Config.DOWNLOAD_LOCATION)

# Check essential configuration
if not Config.BOT_TOKEN:
    logger.error("Please set BOT_TOKEN in config.py or as env var")
    quit(1)

if not Config.API_ID:
    logger.error("Please set API_ID in config.py or as env var")
    quit(1)

if not Config.API_HASH:
    logger.error("Please set API_HASH in config.py or as env var")
    quit(1)

# Initialize bot
bot = Client(
    "All-Url-Uploader",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    workers=50,
    plugins=dict(root="plugins"),
)

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    # Start the bot
    bot.start()
    logger.info("Bot has started.")
    logger.info("**Bot Started**\n\n**Pyrogram Version:** %s \n**Layer:** %s", __version__, layer)
    
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    
    # Keep the bot running and handle idle
    idle()

    # Stop the bot gracefully
    bot.stop()
    logger.info("Bot Stopped ;)")
