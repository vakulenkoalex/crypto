import json


class Config:
    def __init__(self, file_name):
        self._file_name = file_name
        self.log_file = ""
        self.debug = False

        self.bybit_api_key = ""
        self.bybit_api_secret = ""
        self.bybit_testnet = True

        self.telegram_bot_token = ""
        self.telegram_skip_message_seconds = 60
        self.telegram_magic_string = ""

        self.buy_percent_for_tp_sl = 0
        self.sell_percent_for_tp_sl = 0
        self.account_percent_for_quantity = 0
        self.black_list_symbol = []
        self.price_percent = 0
        self.leverage = 1

    def read_config_file(self):
        with open(self._file_name) as conf_file:
            for key, value in json.loads(conf_file.read()).items():
                setattr(self, key, value)
