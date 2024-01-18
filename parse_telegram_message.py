from pybit.unified_trading import HTTP

from by_bit import ByBitOrder
from logger import CryptoLogger
from order import Order
from read_signal import Signal


def parse_message(config, balance, text):
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
        new_bybit = ByBitOrder(config, session, new_order, balance)
        new_bybit.place_order()
    except Exception as e:
        logger.error(f"error: {e}")
