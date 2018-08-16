import logging

from .logger import SocketLogger

error_logger = SocketLogger(logger_name='error', log_level=logging.ERROR).get_logger()
