from enum import Enum

from exception import CryptoException
from logger import CryptoLogger


class Direction(Enum):
    DUMP = 'DUMP: '
    PUMP = 'PUMP: '
    EMPTY = 'EMPTY'


class Signal:
    def __init__(self, config, text):
        self.text = text
        self.direction = Direction.EMPTY
        self.symbol = ''
        self.high_sum = 0
        self.low_sum = 0

        self._letter_start_symbol = '#'
        self._letter_end_symbol = " "
        self._letter_start_sum = '₮ '
        self._letter_end_sum = "\n"

        logger = CryptoLogger("Signal", config.log_file)
        self._parse_text()
        logger.info(f"Create {self}")

    def __format__(self, format_spec):
        return (f"{self.__class__.__name__}:"
                f"direction={self.direction},"
                f"symbol={self.symbol},"
                f"high_sum={self.high_sum},"
                f"low_sum={self.low_sum}")

    def _parse_text(self):
        for element in Direction:
            if self.text.find(element.value) > 0:
                self.direction = Direction(element.value)
                break
        if self.direction == Direction.EMPTY:
            raise CryptoException(self.__class__.__name__, "not found Direction")

        position_direction = self.text.find(self.direction.value + self._letter_start_symbol)
        if position_direction < 0:
            raise CryptoException(self.__class__.__name__, "not found start Symbol")
        position_start_symbol = position_direction + len(self.direction.value) + 1
        position_end_symbol = self.text.find(self._letter_end_symbol, position_start_symbol)
        if position_end_symbol < 0:
            raise CryptoException(self.__class__.__name__, "not found end Symbol")
        self.symbol = self.text[position_start_symbol:position_end_symbol]

        position_high_sum = self.text.find(self._letter_start_sum)
        if position_high_sum < 0:
            raise CryptoException(self.__class__.__name__, "not found start High_sum")
        position_start_high_sum = position_high_sum + 2
        position_end_high_sum = self.text.find(self._letter_end_sum, position_start_high_sum)
        if position_end_high_sum < 0:
            raise CryptoException(self.__class__.__name__, "not found end High_sum")
        self.high_sum = float(self.text[position_start_high_sum:position_end_high_sum])

        position_low_sum = self.text.find(self._letter_start_sum, position_end_high_sum)
        if position_low_sum < 0:
            raise CryptoException(self.__class__.__name__,'not found start Low_sum')
        position_start_low_sum = position_low_sum + 2
        position_end_low_sum = self.text.find(self._letter_end_sum, position_start_low_sum)
        if position_end_low_sum < 0:
            raise CryptoException(self.__class__.__name__,'not found end Low_sum')
        self.low_sum = float(self.text[position_start_low_sum:position_end_low_sum])
