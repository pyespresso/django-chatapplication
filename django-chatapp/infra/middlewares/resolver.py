from uuid import uuid4
from django.urls import resolve
from infra.utils.json import is_json


class Resolver:

  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):

    request_id = str(uuid4())
    setattr(request, 'id', request_id)

    request_body = request.body
    is_body_json, json_body = is_json(request_body.decode('utf-8') if request_body else '{}')

    setattr(request, '_is_body_json', is_body_json)
    setattr(request, '_json_body', json_body if is_body_json else {})

    request_parameters = resolve(request.path_info)
    request.url_info = {
        'kwargs': request_parameters.kwargs,
        'url_name': request_parameters.url_name,
        'app_names': request_parameters.app_names,
        'app_name': request_parameters.app_name,
        'namespaces': request_parameters.namespaces,
        'namespace': request_parameters.namespace,
        'view_name': request_parameters.view_name
    }
    return self.get_response(request)
