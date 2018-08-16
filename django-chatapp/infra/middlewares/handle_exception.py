import traceback

from django.conf import settings
from django.http.response import (
    HttpResponse,
    JsonResponse,
    StreamingHttpResponse,
    HttpResponseNotAllowed
)

# from infra.utils.loggers import error_logger
from infra.utils.http_error import (
    HttpError,
    InternalServerError,
    MethodNotAllowed
)


class HandleException:
    '''Middleware for handling exceptions.

    Attributes:
        get_response: handler method of next middleware or view
    '''

    def __init__(self, get_response):
        self.get_response = get_response

        # overriding Django's inbuilt error handling
        setattr(settings, 'DEBUG_PROPAGATE_EXCEPTIONS', True)

    def __call__(self, request):
        '''Handler method for middleware

        Args:
            request: Django's request object.

        Returns:
            Response passed by next middleware or view.

        '''

        try:
            response = self.get_response(request)

            if isinstance(response, HttpResponseNotAllowed):
                raise MethodNotAllowed

            if isinstance(response, (HttpResponse, StreamingHttpResponse)):
                return response
            else:
                print(response)
                return JsonResponse(response)

        except HttpError as e:
            return e.response

        except Exception as e:
            # log unhandled exception
            error = traceback.format_exc()
            log = '{uuid} :: \n{traceback}\n\n---------------------------------------------------------'.format(
                uuid=request.id,
                traceback=error
            )
            # error_logger.error(log)
            traceback.print_exc()

            # send default error response hiding sensitive exception details
            return InternalServerError().response
