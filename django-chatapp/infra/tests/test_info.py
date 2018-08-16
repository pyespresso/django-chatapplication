from unittest import TestCase
from rest_framework.test import RequestsClient as Client
from django.core.cache import cache
from mock import patch
import json, sys
import urllib.parse


class Info(TestCase):
  '''
  Testing the controller functions only
  '''
  @classmethod
  def setUpClass(cls):
    print("\n" + '\x1b[0;34;40m' + 'Starting API tests...' + '\x1b[0m')

  def setUp(self):
    pass
    self.client = Client()

  def tearDown(self):
    pass

  @classmethod
  def tearDownClass(cls):
    print("Finished API tests...\n")

  def test_01_app_health(self):
    response = self.client.get('http://localhost:8000/')
    self.assertEqual(response.status_code, 404)

  @patch('infra.utils.default_model_manager.DefaultManager.get_one')
  def test_02_api_info(self, mocked):
    account_name = 'ahn'
    params = {'environment': 'production'}
    env = 'production'
    baseURL = 'https://www.datashop.mercyhealthprovider.com/api/v2'
    mocked.side_effect = [
      {
          'type': env,
          'baseURL': baseURL,
          'accountName': account_name
      },
      None
    ]
    response = self.client.get('http://localhost:8000/accounts/{account_name}/info?{q}'.format(
      account_name=account_name, q=urllib.parse.urlencode(params)))
    self.assertDictEqual(
      json.loads(response.content.decode(sys.getdefaultencoding())),
      {
        'type': env,
        'baseURL': baseURL,
        'accountName': account_name
      }
    )

    self.assertEqual(response.status_code, 200)

    response = self.client.get('http://localhost:8000/accounts/{account_name}/info?{q}'.format(
      account_name='AHN', q=urllib.parse.urlencode(params)))
    self.assertEqual(response.status_code, 404)

  @patch('infra.utils.default_model_manager.DefaultManager.get_all')
  def test_03_helpers(self, mocked):
    mocked.side_effect = [
      [
        {
          "routeName" : "info",
          "method" : "GET",
          "isActive" : True,
          "queryParams" : [
            {
              "dataType" : "STRING",
              "isRequired" : True,
              "name" : "environment",
              "enum" : [
                "production",
                "qa",
                "staging"
              ],
              "default" : "production",
              "action" : {
                "actionType" : "IN",
                "value" : [
                  "production",
                  "qa"
                ]
              }
            }
          ]
        }
      ]
    ]

    self.assertDictEqual(cache.get('request_configs').get('info')['GET'], {
        "routeName" : "info",
        "method" : "GET",
        "isActive" : True,
        "queryParams" : [
            {
                "dataType" : "STRING",
                "isRequired" : True,
                "name" : "environment",
                "enum" : [
                    "production",
                    "qa",
                    "staging"
                ],
                "default" : "production",
                "action" : {
                    "actionType" : "IN",
                    "value" : [
                        "production",
                        "qa"
                    ]
                }
            }
        ]})
