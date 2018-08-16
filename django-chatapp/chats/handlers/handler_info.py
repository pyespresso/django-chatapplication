from chats.models.model_info import User, Chunk, Conversation ,Data
from bson import ObjectId
import datetime

class Handler:
    def __init__(self):
        pass

    def comparator(elem):
        return elem['data'][0]['timestamp']

    def getconversationhistory(self,user_id, friends):

        conversation_ids = []  # all conversation ids
        friend_ids = []
        user_id = str(user_id)
        for friend in friends:
            friend = str(friend)
            if user_id < friend:
                conversation_id = user_id + friend  # convesation_id
            else:
                conversation_id = friend + user_id
            friend_ids.append(ObjectId(friend))
            conversation_ids.append(conversation_id)

        chunk_ids = [conversation['chunks'][0] for conversation in Conversation.objects.get_all(queries={'id': {'$in': conversation_ids}},
                                                         projection={'chunks': 1})]
        chunks = Chunk.objects.get_all(queries={'_id': {'$in': list(map((lambda x: ObjectId(x)), chunk_ids))}})
        # print(chunks)
        chunks.sort(key=Handler.comparator, reverse=True)

        friend_objects = User.objects.get_all(queries={'_id':{'$in':friend_ids}},projection={'fname':1})
        # print(friend_objects)
        friend_name = {}
        for friend in friend_objects:
            friend_name[friend['_id']] = friend['fname']

        response = {"data":[]}
        i = 0
        for chunk in chunks:
            response_data = {
                "name" : friend_name[ObjectId(friends[i])],
                "id" : str(chunk["_id"]),
                "message" : chunk["data"]
            }
            response['data'].append(response_data)
            i += 1
        # print(response)
        return(response)

    def send_msg(self,senderID, recipientIDs, fname, message, conversationID, chunk_mapping):

        handler = Handler()

        for recipient in recipientIDs:
            # check if recipent exist as friend
            exists = ObjectId(recipient) in User.objects.get_one(queries={"_id": ObjectId(senderID)})['friends']
            updated = False

            if exists:
                updated = Chunk.objects.update_one(
                    queries={'_id': chunk_mapping[conversationID[recipient]], '$where': 'this.data.length<3'},
                    data={'$push': {'data':
                                        {'$each': [{"timestamp": datetime.datetime.utcnow(), "author": fname,
                                                    "message": message}],
                                         '$position': 0}
                                    }}, upsert=False)

            # either they are not friends or we need a new chunk
            if not updated:
                new_chunk_id = Chunk.objects.insert_one({"data": [Data(datetime.datetime.utcnow(), fname, message)]})['_id']
                Conversation.objects.update_one(
                    queries={'id': conversationID[recipient]},
                    data={'$push': {'chunks': {'$each': [new_chunk_id], '$position': 0}}},
                    upsert=True
                )

            handler.pull_and_push(senderID, recipient)  # updates friendlist
            handler.pull_and_push(recipient, senderID)

    def pull_and_push(self,user1,user2):

        User.objects.update_one(                                        #pull
            queries={'_id': ObjectId(user1)},
            data={'$pull': {'friends': {'$in': [ObjectId(user2)]}}}
        )

        User.objects.update_one(                                        #push
            queries={'_id': ObjectId(user1)},
            data={'$push': {'friends': {'$each': [ObjectId(user2)], '$position': 0}}}
        )