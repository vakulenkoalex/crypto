import math

from exception import CryptoException
from logger import CryptoLogger
from read_signal import Direction


class Order:
    def __init__(self, config, signal):
        self.side = ''
        self.price = 0
        self.take_profit = 0
        self.stop_loss = 0
        self.symbol = signal.symbol
        #self.coin_for_sell = signal.coin_for_sell

        self._signal = signal
        self._config = config
        self._percent = 0

        logger = CryptoLogger("Order", self._config.log_file)
        self.get_side_by_direction()
        self.set_tp_sl()
        logger.info(f"Create {self}")

    def __format__(self, format_spec):
        return (f"{self.__class__.__name__}:"
                f"side={self.side},"
                f"symbol={self.symbol},"
                f"price={self.price},"
                f"take_profit={self.take_profit},"
                f"stop_loss={self.stop_loss}")

    def get_side_by_direction(self):
        if self._signal.direction == Direction.DUMP:
            self.side = 'Buy'
            self.price = self._signal.low_sum
            self._percent = self._config.buy_percent_for_tp_sl
        elif self._signal.direction == Direction.PUMP:
            self.side = 'Sell'
            self.price = self._signal.high_sum
            self._percent = self._config.sell_percent_for_tp_sl
        else:
            raise CryptoException(self.__class__.__name__, "Direction empty")

    def set_tp_sl(self):
        round_count = 10000
        self.take_profit = math.floor(self.price * (100 + self._percent) / 100 * round_count) / round_count
        self.stop_loss = math.ceil(self.price * (100 - self._percent) / 100 * round_count) / round_count
