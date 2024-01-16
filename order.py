import math

from exception import CryptoException
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
        self.get_side_by_direction()
        self.set_tp_sl()

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
            raise CryptoException('direction emty')

    def set_tp_sl(self):
        round_count = 10000
        self.take_profit = math.floor(self.price * (100 + self._percent) / 100 * round_count) / round_count
        self.stop_loss = math.ceil(self.price * (100 - self._percent) / 100 * round_count) / round_count
