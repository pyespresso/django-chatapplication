from django.core.cache import cache
from infra.models.request_validator import RequestValidationConfig


def load_request_configs():

  configs = {}
  for config in RequestValidationConfig.objects.get_all(queries={'isActive': True}, projection={'_id': 0}):
    if config['routeName'] not in configs:
      configs[config['routeName']] = {config['method']: config}
    else:
      configs[config['routeName']][config['method']] = config
  cache.set('request_configs', configs)
