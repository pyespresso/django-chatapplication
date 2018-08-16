import time
from infra.utils.loggers import log_request, log_response


class Logging:
    '''Middleware for logging the incoming request, outgoing response and errors (if any).
    '''

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        '''Handler method for middleware

        Args:
            request: Django's request object.

        Returns:
            Response passed by next middleware or view.

        '''
        request_epoch = time.time()*1000

        request = log_request(request.id, request, request_epoch, request.url_info['view_name'])

        response = self.get_response(request)

        log_response(request.id, request, request_epoch, response)

        return response
