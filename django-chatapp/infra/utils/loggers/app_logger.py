import logging

from .logger import SocketLogger

app_logger = SocketLogger(logger_name='app', log_level=logging.INFO).get_logger()

