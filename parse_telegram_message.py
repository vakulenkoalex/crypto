from pybit.unified_trading import HTTP
import time

from by_bit import ByBit
from config import Config
from logger import CryptoLogger
from order import Order
from read_signal import Signal


def parse_message(text):
    file_config = 'config.json'
    config = Config(file_config)
    config.read_config_file()
    logger = CryptoLogger(config, "parse_message")

    try:
        new_signal = Signal(text)
        logger.debug(f"Create {new_signal}")

        if new_signal.symbol in config.black_list_symbol:
            logger.info(f"symbol in black list ({new_signal})")
            return

        new_order = Order(config, new_signal)
        logger.debug(f"Create {new_order}")

        session = HTTP(
            testnet=config.bybit_testnet,
            api_key=config.bybit_api_key,
            api_secret=config.bybit_api_secret,
        )
        new_bybit = ByBit(config, session, new_order)
        if not new_bybit.place_order():
            return
        for counter in range(config.counter_in_check_order_filled):
            time.sleep(config.pause_in_check_order_filled)
            if new_bybit.check_order_filled():
                break
        logger.info(f"check end {new_bybit}")
    except Exception as e:
        logger.error(f"error: {e}")
