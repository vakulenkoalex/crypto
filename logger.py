import logging


class CryptoLogger:
    def __init__(self, name, log_file):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        if len(self.logger.handlers) == 0:
            file_handler = logging.FileHandler(log_file, encoding='utf8')
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s (%(process)5d) - %(message)s')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)
