from telegram import Update
from flask import Flask, request, jsonify
from flask_cors import CORS
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from service.start import start
from service.button_click import button_click_handler
from service.onmessage import OnMessage
import multiprocessing
import logging
import json


app = Flask(__name__)
CORS(app, origins='*')

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

application = None

def run_bot(token: str) -> None:
    global application
    application = Application.builder().token(token).build()

    # Загружаем данные из data.json
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
        application.bot_data['custom_data'] = data
    except FileNotFoundError:
        logger.error("data.json not found. Setting custom_data to empty dict.")
        application.bot_data['custom_data'] = {}
    except json.JSONDecodeError:
        logger.error("Error decoding data.json. Setting custom_data to empty dict.")
        application.bot_data['custom_data'] = {}

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, OnMessage))
    application.add_handler(CallbackQueryHandler(button_click_handler))

    logger.info("Starting bot polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

@app.route('/start_polling', methods=['POST', 'GET'])
def start_polling():
    data = request.get_json()
    token = data['key']

    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Сохраняем данные в data.json
    with open('data.json', 'w') as f:
        json.dump(data, f)

    p = multiprocessing.Process(target=run_bot, args=(token,))
    p.start()
    return jsonify({"status": "Polling started", "data": data}), 200

@app.route('/stop_polling', methods=['POST'])
def stop_polling():
    global application
    if application is not None:
        application.stop()
        application = None
        return jsonify({"status": "Polling stopped"}), 200
    else:
        return jsonify({"error": "Polling was not running"}), 200

if __name__ == "__main__":
    app.run(port=5000)
