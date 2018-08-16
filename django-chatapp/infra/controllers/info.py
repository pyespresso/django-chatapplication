from django.views.decorators.http import require_http_methods

from infra.models.info import Info
from infra.utils.response import OK
from infra.utils.http_error import NotFound


@require_http_methods(["GET"])
def info(request, account_name):
  b = Info.objects.get_one(
    queries={'accountName': account_name, 'environments.type': request.GET.get('environment')},
    projection={'accountName': 1, 'environments.$': 1, '_id': 0}, filters={}
  )
  if b:
    return OK(data=b)
  else:
    raise NotFound(
      errors={
        "error": {
          "message": "Account Info or Environment details doesn't exist",
          "code": 404
        }
      }
    )
