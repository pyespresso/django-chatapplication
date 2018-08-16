import time
from .logger import SocketLogger

response_logger = SocketLogger(logger_name='response').get_logger()


def log_response(request_id, request, request_epoch, response):
    '''Method to log outgoing response.

    Args:
        request_id: Request's unique id.
        request: Request object.
        request_epoch: Epoch time when request has to be logged.
        response: Response object.
    '''

    response_epoch = time.time() * 1000
    content = bytes(response.content if response.status_code / 100 != 2 else b'{}')

    log = (
        '{uuid} ::{host} {timestamp} :: {user_id} :: No Session :: :: {response_body} :: {response_status_code}'
        ' :: {response_time} :: {response_size_bytes} :: {cache_status}'.format(
            uuid=request_id,
            timestamp=str(response_epoch),
            user_id=(
                (request.user_data or {}).get('user_id', 'User info not available')
                if hasattr(request, 'user_data') else 'User info not extracted'
            ),
            host=request.META.get('SERVER_NAME'),
            response_body=content.decode('utf-8'),
            response_status_code=response.status_code,
            response_time=str(response_epoch - request_epoch),
            response_size_bytes=len(content),
            cache_status='No cache'  # to be updated if caching is used
        )
    )

    response_logger.info(log)
