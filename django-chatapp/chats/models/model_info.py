from pymodm import EmbeddedMongoModel, MongoModel, fields
from infra.utils.default_model_manager import DefaultManager
from pymodm.manager import Manager
import datetime


class User(MongoModel):
    id = fields.CharField()
    fname = fields.CharField()
    lname = fields.CharField()
    friends = fields.ListField(blank=True)
    objects = DefaultManager()


class Conversation(MongoModel):
    id = fields.CharField() #Example: ankur-priyanshu
    chunks = fields.ListField() #LIST of chunk _id
    objects = DefaultManager()

class Data(EmbeddedMongoModel):
    timestamp=fields.DateTimeField(default=datetime.datetime.utcnow())
    author = fields.CharField()
    message = fields.CharField()

class Chunk(MongoModel):
    id = fields.CharField()
    data = fields.EmbeddedDocumentListField(model=Data) #LIST
    objects = DefaultManager()
