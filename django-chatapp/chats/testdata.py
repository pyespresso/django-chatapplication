from infra.utils.helpers import load_request_configs
from django.conf import settings
from chats.models.model_info import User,Conversation,Chunk, Data
from pymodm import EmbeddedMongoModel, MongoModel, fields
from infra.utils.default_model_manager import DefaultManager
from pymodm.manager import Manager
import datetime

#User.objects.remove()
# Conversation.objects.remove()
# Chunk.objects.remove()
# User.objects.remove()
#
# User(_id="5b689bc92979917d2be6a9ed",fname="priyanshu",lname="kumar",friends=["5b689bc92979917d2be6a9ee","5b689bc92979917d2be6a9ef"]).save()
# User(_id="5b689bc92979917d2be6a9ee",fname="ankur",lname="jain",friends=["5b689bc92979917d2be6a9ed","5b689bc92979917d2be6a9ef"]).save()
# User(_id="5b689bc92979917d2be6a9ef",fname="mandar",lname="gondhalekar",friends=["5b689bc92979917d2be6a9ed","5b689bc92979917d2be6a9ee"]).save()
#
# Conversation(id="5b689bc92979917d2be6a9ee5b689bc92979917d2be6a9ef",chunks=["5b69b8a9297991615abe4253"]).save()
# Conversation(id="5b689bc92979917d2be6a9ed5b689bc92979917d2be6a9ef",chunks=["5b69b8a9297991615abe4255"]).save()
# Conversation(id="5b689bc92979917d2be6a9ed5b689bc92979917d2be6a9ee",chunks=["5b69b8a9297991615abe4252",
#                                                                            "5b69b8a9297991615abe4254"]).save()

#
# data1 = {"author":"ankur","message":"GoT kab aa raha hai?"}
# data2 = {"author":"priyanshu","message":"mai GoT nahi dekhta"}
# data3 = {"author":"mandar","message":"mai GoT nahi dekhta"}
# data4 = {"author":"priyanshu","message":"Am I socially acceptable? :P "}
# data5 = {"author":"ankur","message":"No, Not at all"}
# data6 = {"author":"mandar","message":"mai hot girls wanted dekhta hun"}
# data7 = {"author":"priyanshu","message":"How you doin!"}
# data8 = {"author":"priyanshu","message":"GoT kaun hi dekhta hai be"}
#
# Chunk(_id="5b69b8a9297991615abe4252",data=[data7,
#          data5,
#          ]).save()
#
# Chunk(_id="5b69b8a9297991615abe4253",data=[data1,
#          data3,
#          data6]).save()
#
# Chunk(_id="5b69b8a9297991615abe4254",data=[data1,
#          data2,
#          data4]).save()
#
# Chunk(_id="5b69b8a9297991615abe4255",data=[data3,
#          data6,
#          data8]).save()




# print("\n\nAll user objects====>\n")
# user_collec=User.objects.get_all()
# for dict in user_collec:
#     print(dict)
#
# # print("\n\nAll Conversation objects====>\n")
# # Conversation_collec=Conversation.objects.get_all()
# # for dict in Conversation_collec:
# #     print(dict)
#
# print("\n\nAll Chunk objects====>\n")
# Chunk_collec=Chunk.objects.get_all()
# for dict in Chunk_collec:
#     print(dict)
