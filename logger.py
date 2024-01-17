import logging
import sys


class CryptoLogger:
    def __init__(self, config, name):
        self.logger = logging.getLogger(name)
        if config.debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

        if len(self.logger.handlers) == 0:
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s (%(process)5d) - %(message)s')
            file_handler = logging.FileHandler(config.log_file, encoding='utf8')
            self.logger.addHandler(file_handler)
            self.logger.addHandler(logging.StreamHandler(sys.stdout))
            for element in self.logger.handlers:
                element.setFormatter(formatter)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)
