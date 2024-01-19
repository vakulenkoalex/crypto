import datetime

import pytz
from pybit.unified_trading import HTTP
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes

import parse_telegram_message
from config import Config
from logger import CryptoLogger
from by_bit import ByBitBalance

file_config = 'config.json'
config = Config(file_config)
config.read_config_file()
logger = CryptoLogger(config, "telegram_message")

session = HTTP(
            testnet=config.bybit_testnet,
            api_key=config.bybit_api_key,
            api_secret=config.bybit_api_secret,
        )
new_balance = ByBitBalance(config, session)
balance = new_balance.get_balance()


async def get_text_form_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    logger.info(f"Get message '{message.text}' (id={message.id}, date={message.date})")
    delta = (datetime.datetime.now(pytz.utc) - message.date).total_seconds()
    logger.debug(f"time delta {delta}")
    if delta > config.telegram_skip_message_seconds:
        logger.info(f"Skip message by date id={message.id}")
        return
    if config.telegram_magic_string != "" and message.text.find(config.telegram_magic_string) == -1:
        logger.info(f"Skip message by string id={message.id}")
        return

    parse_telegram_message.parse_message(config, balance, message.text)


logger.info("Start listen")
application = ApplicationBuilder().token(config.telegram_bot_token).build()
echo_handler = MessageHandler(filters.TEXT, get_text_form_message)
application.add_handler(echo_handler)
application.run_polling()
