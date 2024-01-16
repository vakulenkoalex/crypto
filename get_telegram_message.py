from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes

from config import Config
import parse_telegram_message
from logger import CryptoLogger


file_config = 'config.json'
config = Config(file_config)
config.read_config_file()
logger = CryptoLogger("telegram_message", config.log_file)

async def get_text_form_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    logger.info(f"Get message '{message.text}'")
    # parse_telegram_message.parse_message(message.text)


logger.info("Start listen")
application = ApplicationBuilder().token(config.telegram_bot_token).build()
echo_handler = MessageHandler(filters.TEXT, get_text_form_message)
application.add_handler(echo_handler)
application.run_polling()
