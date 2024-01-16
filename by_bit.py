from exception import CryptoException
from logger import CryptoLogger


class ByBit:
    def __init__(self, config, session, order):
        self._config = config
        self._session = session
        self._order = order
        self._logger = CryptoLogger("ByBit", config.log_file)

    def __format__(self, format_spec):
        return (f"{self.__class__.__name__}:"
                f"order={self._order}")

    def _find_open_order(self):
        result = False
        open_statuses = ["Created", "New", "PartiallyFilled"]

        reply = self._session.get_open_orders(
                    category="linear",
                    symbol=self._order.symbol,
                    openOnly=0,
                    limit=1,
                )
        self._logger.info(f"bybit_request_get_open_orders: {reply}")

        if reply["retCode"] == 0:
            reply_list = reply["result"]["list"]
            if len(reply_list) > 0:
                reply_order = reply_list[0]
                result = reply_order["orderStatus"] in open_statuses
        else:
            raise CryptoException(self.__class__.__name__, "retCode not find")

        self._logger.info(f"find_open_order: {result}")
        return result

    def _get_quantity(self):
        # TODO нужен алгоритм расчета баланса
        reply = self._session.get_wallet_balance(
            accountType="UNIFIED",
            coin="USDT",
        )
        self._logger.info(f"bybit_request_get_wallet_balance {reply}")

        result = 10 * self._config.account_percent_for_quantity / 100

        self._logger.info(f"get_quantity: {result}")
        return result

    def place_order(self):
        if self._find_open_order():
            return

        quantity = self._get_quantity()
        reply = self._session.place_order(
                orderType="Limit",
                category="linear",
                timeInForce="GTC",
                symbol=self._order.symbol,
                side=self._order.side,
                qty=quantity,
                price=self._order.price,
                takeProfit=f'{self._order.take_profit}',
                stopLoss=f'{self._order.stop_loss}'
            )
        self._logger.info(f"bybit_request_place_order {reply}")
