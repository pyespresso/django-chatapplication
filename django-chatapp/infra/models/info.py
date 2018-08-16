from pymodm import EmbeddedMongoModel, MongoModel, fields
from infra.utils.default_model_manager import DefaultManager


class Environments(EmbeddedMongoModel):
  baseURL = fields.CharField(required=True)
  type = fields.CharField(required=True, max_length=20)


class Info(MongoModel):
  accountName = fields.CharField(max_length=60, required=True)
  environments = fields.EmbeddedDocumentListField(model=Environments)
  objects = DefaultManager()
  # oo = Manager().
  class Meta:
    collection_name = 'Info'
    final = True
