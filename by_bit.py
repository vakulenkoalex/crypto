import math

from exception import CryptoException
from logger import CryptoLogger


def valid_result_api(self, reply):
    if reply["retCode"] != 0:
        raise self._exception("_valid_result_api retCode not 0")


class ByBitOrder:
    def __init__(self, config, session, order, balance):
        self._config = config
        self._session = session
        self._order = order
        self._logger = CryptoLogger(config, self.__class__.__name__)
        self._orderId = None
        self._quantity = None
        self._balance = balance

    def __format__(self, format_spec):
        return (f"{self.__class__.__name__}:"
                f"side={self._order.side},"
                f"symbol={self._order.symbol},"
                f"price={self._order.price},"
                f"take_profit={self._order.take_profit},"
                f"stop_loss={self._order.stop_loss},"
                f"quantity={self._quantity},"
                f"orderId={self._orderId}")

    def place_order(self):
        if self._find_open_order():
            self._logger.info(f"find open order {self}")
            return False

        self._set_quantity()
        self._logger.info(f"start place_order: {self}")
        reply = self._session.place_order(
                orderType="Limit",
                category="linear",
                timeInForce="GTC",
                symbol=self._order.symbol,
                side=self._order.side,
                qty=self._quantity,
                price=self._order.price,
                takeProfit=f'{self._order.take_profit}',
                stopLoss=f'{self._order.stop_loss}'
            )
        self._logger.debug(f"bybit_place_order {reply}")

        valid_result_api(reply)
        self._orderId = reply["result"]["orderId"]
        self._logger.info(f"end place_order: {self}")

        return True

    def check_order_filled(self):
        self._logger.info(f"check_order_filled {self}")
        if self._orderId == "":
            raise self._exception("_orderId empty")

        filled_statuses = ["Filled"]
        result = self._order_in_status(filled_statuses, orderId=self._orderId)
        if result is None:
            raise self._exception("check_order_filled result.list empty")

        self._logger.info(f"check_order_filled_result {result} ({self})")
        return result

    def _find_open_order(self):
        open_statuses = ["Created", "New", "PartiallyFilled"]
        result = self._order_in_status(open_statuses, symbol=self._order.symbol, openOnly=0)
        if result is None:
            return False
        else:
            return result

    def _set_quantity(self):
        sum_balance = self._balance * self._config.account_percent_for_quantity / 100
        result = math.floor(sum_balance / self._order.price)

        self._logger.info(f"get_quantity: {result}")
        self._quantity = result

    def _order_in_status(self, statuses, **kwargs):
        reply = self._session.get_open_orders(
                    category="linear",
                    limit=1,
                    **kwargs
                )
        self._logger.debug(f"bybit_get_open_orders: {reply}")

        reply_order = self._get_result_from_api(reply)
        if reply_order is None:
            result = None
        else:
            result = reply_order["orderStatus"] in statuses

        return result

    def _get_result_from_api(self, reply):
        valid_result_api(reply)
        reply_list = reply["result"]["list"]
        if len(reply_list) == 0:
            return None

        return reply_list[0]

    def _exception(self, message):
        return CryptoException(self.__class__.__name__, message)


class ByBitBalance:
    def __init__(self, config, session):
        self._config = config
        self._session = session
        self._logger = CryptoLogger(config, self.__class__.__name__)

    def get_balance(self):
        reply = self._session.get_wallet_balance(
            accountType="UNIFIED",
            coin="USDT",
        )
        self._logger.debug(f"get_balance_bybit_get_wallet_balance {reply}")
        valid_result_api(reply)
        balance = float(reply['result']['list'][0]['coin'][0]['walletBalance'])
        self._logger.info(f"get_balance {balance}")

        return balance
