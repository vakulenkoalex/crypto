from exception import CryptoException
from logger import CryptoLogger


class ByBit:
    def __init__(self, config, session, order):
        self._config = config
        self._session = session
        self._order = order
        self._logger = CryptoLogger("ByBit", config.log_file)
        self._orderId = None
        self._quantity = None

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
        self._logger.info(f"bybit_request_place_order: {self}")
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
        self._logger.info(f"bybit_request_place_order {reply}")

        reply_order = self._get_result_from_api(reply)
        if reply_order is None:
            raise self._exception("place_order result.list empty")
        self._orderId = reply_order.orderId

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
        # TODO нужен алгоритм расчета баланса
        reply = self._session.get_wallet_balance(
            accountType="UNIFIED",
            coin="USDT",
        )
        self._logger.info(f"get_quantity_bybit_request_get_wallet_balance {reply}")

        result = 10 * self._config.account_percent_for_quantity / 100

        self._logger.info(f"get_quantity: {result}")
        self._quantity = result

    def _order_in_status(self, statuses, **kwargs):
        reply = self._session.get_open_orders(
                    category="linear",
                    limit=1,
                    **kwargs
                )
        self._logger.info(f"bybit_request_get_open_orders: {reply}")

        reply_order = self._get_result_from_api(reply)
        if reply_order is None:
            result = None
        else:
            result = reply_order["orderStatus"] in statuses

        return result

    def _get_result_from_api(self, reply):
        if reply["retCode"] != 0:
            raise self._exception("get_result_from_api retCode not 0")
        reply_list = reply["result"]["list"]
        if len(reply_list) == 0:
            return None

        return reply_list[0]

    def _exception(self, message):
        return CryptoException(self.__class__.__name__, message)
