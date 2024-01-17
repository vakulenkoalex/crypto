import datetime

import pytz
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes

import parse_telegram_message
from config import Config
from logger import CryptoLogger

file_config = 'config.json'
config = Config(file_config)
config.read_config_file()
logger = CryptoLogger(config,"telegram_message")

async def get_text_form_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    logger.info(f"Get message '{message.text}' (id={message.id}, date={message.date})")
    if (datetime.datetime.now(pytz.utc) -message.date).seconds > config.telegram_skip_message_seconds:
        logger.info(f"Skip message id={message.id}")
        return
    parse_telegram_message.parse_message(message.text)


logger.info("Start listen")
application = ApplicationBuilder().token(config.telegram_bot_token).build()
echo_handler = MessageHandler(filters.TEXT, get_text_form_message)
application.add_handler(echo_handler)
application.run_polling()
