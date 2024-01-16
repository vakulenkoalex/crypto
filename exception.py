
class CryptoException(Exception):
    def __init__(self, class_name, message):
        self._class_name = class_name
        self._message = message

    def __format__(self, format_spec):
        return f'{self._message} ({self._class_name}))'
