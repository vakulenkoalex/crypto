from exception import CryptoException


class ByBit:
    def __init__(self, config, session, order):
        self._config = config
        self._session = session
        self._order = order

    def _find_open_order(self):
        result = False
        open_statuses = ["Created", "New", "PartiallyFilled"]

        reply = self._session.get_open_orders(
                    category="linear",
                    symbol=self._order.symbol,
                    openOnly=0,
                    limit=1,
                )

        if reply["retCode"] == 0:
            reply_list = reply["result"]["list"]
            if len(reply_list) > 0:
                reply_order = reply_list[0]
                result = reply_order["orderStatus"] in open_statuses
        else:
            raise CryptoException('retCode not find')

        return result

    def _get_quantity(self):
        # balance = self._session.get_wallet_balance(
        #     accountType="UNIFIED",
        #     coin=self._order.coin_for_sell,
        # )
        return 10 * self._config.account_percent_for_quantity / 100

    def place_order(self):
        if self._find_open_order():
            return

        quantity = self._get_quantity()
        a = self._session.place_order(
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
        print(a)
