from pybit.unified_trading import HTTP

from by_bit import ByBit
from config import Config
from order import Order
from read_signal import Signal


def parse_message(text):
    file_config = 'config.json'
    config = Config(file_config)
    config.read_config_file()

    session = HTTP(
                testnet=config.bybit_testnet,
                api_key=config.bybit_api_key,
                api_secret=config.bybit_api_secret,
            )
    new_signal = Signal(text)
    new_order = Order(config, new_signal)
    ByBit(config, session, new_order).place_order()
