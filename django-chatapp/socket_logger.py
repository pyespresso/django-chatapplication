import pickle
import logging
import logging.handlers
import socketserver
import struct
import os
import time

logger_info = {}


class FileLogger:
  def __init__(self, logger_name, file_name=None, is_access=False):

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    if not file_name:
      file_name = 'applog'
    file_name += ".log"

    # create logs directory if not available
    if not os.path.exists("logs/"):
      os.makedirs("logs/")
    fh = logging.handlers.TimedRotatingFileHandler("logs/" + file_name, when='MIDNIGHT', utc=True)

    if is_access:
      fh.setLevel(logging.INFO)
    else:
      fh.setLevel(logging.DEBUG)

    logger.addHandler(fh)
    self.logger = logger

  def get_logger(self):
    return self.logger


class LogRecordStreamHandler(socketserver.StreamRequestHandler):
  """Handler for a streaming logging request.

  This basically logs the record using whatever logging policy is
  configured locally.
  # """

  def handle(self):
    """
    Handle multiple requests - each expected to be a 4-byte length,
    followed by the LogRecord in pickle format. Logs the record
    according to whatever policy is configured locally.
    """

    while True:
      chunk = self.connection.recv(4)
      if len(chunk) < 4:
        break
      slen = struct.unpack('>L', chunk)[0]
      chunk = self.connection.recv(slen)
      while len(chunk) < slen:
        chunk = chunk + self.connection.recv(slen - len(chunk))
      obj = self.unPickle(chunk)

      log = "PID: {process} > {time} - {name} - {levelname} - [{module} - {funcName}()] - {msg}".format(
        process=obj['process'],
        time=time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(obj['created'])),
        name=obj['name'],
        levelname=obj['levelname'],
        module=obj['module'],
        funcName=obj['funcName'],
        msg=obj['msg'])
      self.handleLogRecord(log, obj['name'], obj['levelname'])

  def unPickle(self, data):
    return pickle.loads(data)

  def handleLogRecord(self, record, logger_name, levelname):

    if self.server.logname is not None:
      name = self.server.logname
    else:
      name = logger_name

    if not (name in logger_info):
      logger_info.update(
        {
          name: FileLogger(logger_name=name, file_name=None if name=="custom" else name,
                           is_access=True if name=="access" else False).get_logger()
        }
      )

    if levelname == 'DEBUG':
      logger_info[name].debug(record)
    elif levelname == 'ERROR':
      logger_info[name].error(record)
    elif levelname == 'CRITICAL':
      logger_info[name].fatal(record)
    elif levelname == 'WARNING':
      logger_info[name].warn(record)
    else:
      logger_info[name].info(record)


class LogRecordSocketReceiver(socketserver.ThreadingTCPServer):
  """
  Simple TCP socket-based logging receiver suitable for testing.
  """

  allow_reuse_address = 1

  # TODO: Move socket configs to config.py
  def __init__(self, host='localhost',
               port=logging.handlers.DEFAULT_TCP_LOGGING_PORT,
               handler=LogRecordStreamHandler):

    socketserver.ThreadingTCPServer.__init__(self, (host, port), handler)
    self.abort = 0
    self.timeout = 1
    self.logname = None

  def serve_until_stopped(self):
    import select
    abort = 0
    while not abort:
      rd, wr, ex = select.select([self.socket.fileno()],
                                 [], [],
                                 self.timeout)
      if rd:
        self.handle_request()
      abort = self.abort


def socket_logger():
  tcpserver = LogRecordSocketReceiver()

  print('Started TCP Logger server...')
  tcpserver.serve_until_stopped()


if __name__ == '__main__':

  pid = str(os.getpid())
  pidfile = 'socket_logger.pid'

  if not os.path.exists("supervisor/"):
    os.makedirs("supervisor/")
  filename = os.path.join(os.path.abspath('supervisor'), pidfile)
  with open(filename, 'w') as f:
    f.write(pid)
  socket_logger()
