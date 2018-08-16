import os
import logging
import logging.handlers
from django.conf import settings


class ContextFilter(logging.Filter):
  """
  Add Context Info for every log record can be done here
  """
  def filter(self, record):
    # Fetch Request ID for every request
    record.request_id = record.request.id
    record.msg = (record.request.id or '') + " :: " + record.getMessage()
    return True


class SocketLogger:

  def __init__(self, logger_name, log_level=logging.DEBUG):
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    socket_handler = logging.handlers.SocketHandler(settings.LOGGER_SOCKET_IP, settings.LOGGER_SOCKET_PORT)

    pid = os.getpid()

    log_format = "PID: " + str(pid) + "> %(asctime)s - %(name)s - %(levelname)s - [%(module)s - %(funcName)20s()] - " \
                                      "(message)s"
    if logger_name == 'app':
      socket_handler.addFilter(ContextFilter())
    log_format = log_format.format(sub_format=log_format)
    socket_handler.setFormatter(log_format)
    logger.addHandler(socket_handler)
    self.logger = logger

  def get_logger(self):
    return self.logger
