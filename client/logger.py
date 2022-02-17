import datetime
import logging
import os
import os.path
import sys

from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['level'] = record.levelname
        # log_record['namespace'] = service_namespace
        # log_record['sub_name'] = record.name


def formatter_factory():
    return CustomJsonFormatter(fmt='%(asctime)s %(level)s %(message)s')


class SrvLoggerFactory:

    my_formatter = formatter_factory()

    def __init__(self, name='PILOT_SDK'):
        if not os.path.exists('./logs/'):
            os.makedirs('./logs/')
        self.name = name

    def get_logger(self):
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.DEBUG)

        if not logger.handlers:

            # File Handler
            handler = logging.FileHandler('logs/{}.log'.format(self.name))
            handler.setFormatter(self.my_formatter)
            handler.setLevel(logging.DEBUG)

            # Standard Out Handler
            stdout_handler = logging.StreamHandler(sys.stdout)
            stdout_handler.setFormatter(self.my_formatter)
            stdout_handler.setLevel(logging.DEBUG)

            # Standard Err Handler
            stderr_handler = logging.StreamHandler(sys.stderr)
            stderr_handler.setFormatter(self.my_formatter)
            stderr_handler.setLevel(logging.ERROR)

            # register handlers
            logger.addHandler(handler)
            logger.addHandler(stdout_handler)
            logger.addHandler(stderr_handler)

        return logger
