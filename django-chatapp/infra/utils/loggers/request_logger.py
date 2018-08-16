from json import dumps
from infra.utils.json import is_json
from .logger import SocketLogger

request_logger = SocketLogger(logger_name='request').get_logger()


def log_request(request_id, request, request_epoch, request_view_name='unknown'):
    '''Method to log incoming request.

    Args:
        request_id: Request's unique id.
        request: Request object.
        request_epoch: Epoch time when request has to be logged.
        request_view_name: Name of route/view invoked.

    Returns:
        Django HttpRequest object
    '''

    request_body = request.body
    is_body_json, json_body = is_json(request_body.decode('utf-8') if request_body else '{}')
    setattr(request, '_is_body_json', is_body_json)
    setattr(request, '_json_body', json_body if is_body_json else {})

    log = (
        '{uuid} :: {host} {timestamp} :: Check response for user id :: No Session :: {route_name}  ::'
        '{method} {path} :: {query_params} :: {post_body} :: {token} :: {client_addr} :: {user_agent}'.format(
            uuid=request_id,
            timestamp=str(request_epoch),
            post_body=dumps(json_body),
            query_params=dumps(dict(request.GET.lists())),
            path=request.path,
            host=request.META.get('SERVER_NAME'),
            token=request.META.get('HTTP_AUTHORIZATION'),
            user_agent=request.META.get('HTTP_USER_AGENT'),
            client_addr=request.META.get('REMOTE_ADDR'),
            method=request.method,
            route_name=request_view_name
        )
    )

    request_logger.info(log)

    return request
