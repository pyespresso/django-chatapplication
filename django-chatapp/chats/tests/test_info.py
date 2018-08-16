from django.test import TestCase
from unittest import TestCase
from rest_framework.test import RequestsClient as Client
from django.core.cache import cache
from mock import patch
import json, sys
from bson import ObjectId
import datetime
from chats.handlers.handler_info import Handler
import urllib.parse
#   import HttpError

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

  @patch('infra.utils.default_model_manager.DefaultManager.get_all')
  def test_01_api_users(self,mocked):
      user1 = {"_id":ObjectId("5b689bc92979917d2be6a9ef"),"fname":"mandar","lname":"gondhalekar"}
      user2 = {"_id":ObjectId("5b689bc92979917d2be6a9ee"),"fname":"ankur","lname":"jain"}
      user3 = {"_id":ObjectId("5b689bc92979917d2be6a9ed"),"fname":"priyanshu","lname":"kumar"}

      mocked.side_effect = [[user3,user2,user1], []]

      response = self.client.get('http://localhost:8000/users')
      print("users test running.....")

      self.assertDictEqual(
        json.loads(response.content.decode(sys.getdefaultencoding())),
        {
            "data": [
                {
                    "fname": "priyanshu",
                    "id": "5b689bc92979917d2be6a9ed",
                    "lname": "kumar"
                },
                {
                    "fname": "ankur",
                    "id": "5b689bc92979917d2be6a9ee",
                    "lname": "jain"
                },
                {
                    "fname": "mandar",
                    "id": "5b689bc92979917d2be6a9ef",
                    "lname": "gondhalekar"
                }
            ]
        }
      )
      self.assertEqual(response.status_code, 200)

      response = self.client.get('http://localhost:8000/users')

      self.assertDictEqual(
        json.loads(response.content.decode(sys.getdefaultencoding())),
        {
            "statusCode": 404,
            "error": {
                "message": "The resource you are looking for does not exist."
            }
        }
      )
      self.assertEqual(response.status_code, 404)


  @patch('infra.utils.default_model_manager.DefaultManager.get_all')
  def test_02_method_getconversationhistory(self,mocked):
      mocked.side_effect = [

          [{"chunks": [ "5b69c081297991682a83e341", "5b69bf6729799167339482e5", "5b69b8a9297991615abe4253" ]},
           {"chunks": [ "5b69b8a9297991615abe4255" ]},
           {"chunks": [ "5b69c081297991682a83e340", "5b69bf6729799167339482e4", "5b69b8a9297991615abe4252", "5b69b8a9297991615abe4254"]}],

          [{'_id': ObjectId('5b69c081297991682a83e340'), 'data': [{'message': 'hi there!', '_cls': 'chats.models.model_info.Data',
               'timestamp': datetime.datetime(2018, 8, 7, 15, 53, 37, 611000), 'author': 'ankur'}], '_cls': 'chats.models.model_info.Chunk'},
           {'_id': ObjectId('5b69c081297991682a83e341'), 'data': [{'message': 'hi there!', '_cls': 'chats.models.model_info.Data',
               'timestamp': datetime.datetime(2018, 8, 7, 15, 53, 37, 617000), 'author': 'ankur'}],'_cls': 'chats.models.model_info.Chunk'}],

          [{'fname': 'priyanshu', '_id': ObjectId('5b689bc92979917d2be6a9ed')},
           {'fname': 'mandar', '_id': ObjectId('5b689bc92979917d2be6a9ef')}]

      ]

      senderID = "5b689bc92979917d2be6a9ee"
      friends = ["5b689bc92979917d2be6a9ed", "5b689bc92979917d2be6a9ef"]

      handler = Handler()
      self.assertDictEqual(handler.getconversationhistory(senderID,friends),{
          'data': [{'id': '5b69c081297991682a83e341', 'message': [{'message': 'hi there!',
                    'timestamp': datetime.datetime(2018, 8, 7, 15, 53, 37, 617000),'author': 'ankur',
                    '_cls': 'chats.models.model_info.Data'}], 'name': 'priyanshu'},
                    {'id': '5b69c081297991682a83e340', 'message': [{'message': 'hi there!',
                    'timestamp': datetime.datetime(2018, 8, 7, 15, 53, 37, 611000),'author': 'ankur',
                    '_cls': 'chats.models.model_info.Data'}], 'name': 'mandar'}]}
      )

  @patch('chats.handlers.handler_info.Handler.getconversationhistory')
  @patch('infra.utils.default_model_manager.DefaultManager.get_one')
  def test_03_api_history(self,mocked,mocked_getconversationhhistory):

      mocked.side_effect = [
          {},

          {'friends': [ObjectId('5b689bc92979917d2be6a9ef'), ObjectId('5b689bc92979917d2be6a9ed'),
                       '5b689bc92979917d2be6a9ed', '5b689bc92979917d2be6a9ef']},
      ]
      headers = {"id":"5b689bc92979917d2be6a9ee"}

      response = self.client.get('http://localhost:8000/history?user=5b689bc92979917d2be6a9ed',headers = headers)
      self.assertEqual(response.status_code, 404)

      mocked_getconversationhhistory.return_value = {
              "data": [
                  {
                      "id": "5b717ff029799177359b61fa",
                      "name": "mandar",
                      "message": [
                          {
                              "timestamp": "13:06:49 13/08/2018",
                              "author": "ankur",
                              "message": "this code sucks really bad :( "
                          },
                          {
                              "timestamp": "12:56:16 13/08/2018",
                              "author": "ankur",
                              "message": "happy independence day! :)",
                              "_cls": "chats.models.model_info.Data"
                          }
                      ]
                  },
                  {
                      "id": "5b717ff029799177359b61f9",
                      "name": "priyanshu",
                      "message": [
                          {
                              "timestamp": "13:06:49 13/08/2018",
                              "author": "ankur",
                              "message": "this code sucks really bad :( "
                          },
                          {
                              "timestamp": "12:56:16 13/08/2018",
                              "author": "ankur",
                              "message": "happy independence day! :)",
                              "_cls": "chats.models.model_info.Data"
                          }
                      ]
                  }
              ]
          }

      response = self.client.get('http://localhost:8000/history?user=5b689bc92979917d2be6a9ed',headers = headers)
      self.assertDictEqual(
          json.loads(response.content.decode(sys.getdefaultencoding())),
          {
              "data": [
                  {
                      "id": "5b717ff029799177359b61fa",
                      "name": "mandar",
                      "message": [
                          {
                              "timestamp": "13:06:49 13/08/2018",
                              "author": "ankur",
                              "message": "this code sucks really bad :( "
                          },
                          {
                              "timestamp": "12:56:16 13/08/2018",
                              "author": "ankur",
                              "message": "happy independence day! :)",
                              "_cls": "chats.models.model_info.Data"
                          }
                      ]
                  },
                  {
                      "id": "5b717ff029799177359b61f9",
                      "name": "priyanshu",
                      "message": [
                          {
                              "timestamp": "13:06:49 13/08/2018",
                              "author": "ankur",
                              "message": "this code sucks really bad :( "
                          },
                          {
                              "timestamp": "12:56:16 13/08/2018",
                              "author": "ankur",
                              "message": "happy independence day! :)",
                              "_cls": "chats.models.model_info.Data"
                          }
                      ]
                  }
              ]
          }
      )
      self.assertEqual(response.status_code, 200)


  @patch('chats.handlers.handler_info.Handler.send_msg')
  @patch('infra.utils.default_model_manager.DefaultManager.get_one')
  @patch('infra.utils.default_model_manager.DefaultManager.get_all')
  def test_04_api_message(self,mocked_all,mocked_getone,mocked_sendmsg):

      mocked_all.side_effect = [

          [{"_id": ObjectId("5b689bc92979917d2be6a9ed")}, {"_id" : ObjectId("5b689bc92979917d2be6a9ee")},
           {"_id" : ObjectId("5b689bc92979917d2be6a9ef")}],

          #after 404
          [{"_id": ObjectId("5b689bc92979917d2be6a9ed")}, {"_id": ObjectId("5b689bc92979917d2be6a9ee")},
           {"_id": ObjectId("5b689bc92979917d2be6a9ef")}],

          [{"_id": ObjectId("5b689bc92979917d2be6a9ed")}, {"_id": ObjectId("5b689bc92979917d2be6a9ef")}],

          []
      ]

      mocked_getone.return_value = {'fname': 'ankur'}
      mocked_sendmsg.return_value = {}

      headers = {"id":"5b689bc92979917d2be6a9ee", "Content-Type": "application/json"}
      body = {"destination" : ["5b689bc92979917d2be6a9ed","5b689bc92979917d2be6a9eg"],
              "data" : "this code sucks really bad :( ", "broadcast":0}

      response = self.client.put('http://localhost:8000/message',data = json.dumps(body), headers = headers)
      self.assertEqual(response.status_code, 404)

      body = {"destination" : ["5b689bc92979917d2be6a9ed","5b689bc92979917d2be6a9ef"],
              "data": "this code sucks really bad :( ", "broadcast": 1}
      response = self.client.put('http://localhost:8000/message',data = json.dumps(body), headers = headers)
      self.assertEqual(response.status_code, 200)



