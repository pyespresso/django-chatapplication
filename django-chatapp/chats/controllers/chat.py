# stores API endpoints
import json
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from infra.utils.response import OK
from infra.utils.http_error import NotFound
from chats.models.model_info import User, Conversation
from bson import ObjectId
from chats.handlers.handler_info import Handler

@require_http_methods(["GET"])
def users(request):

    users = User.objects.get_all(projection={'fname':1,'lname':1,'_id':1,})

    for user in users:
        user["id"] = user["_id"]
        del user["_id"]

    users_data = {"data" : users}

    if users:
        return OK(data = users_data)
    else:
        raise NotFound()


# @require_http_methods(["GET"])
# def conversation(request):
#
#     conversation = Conversation.objects.get_all(projection={'id':1,'chunks':1,'_id':0})
#     conversation_data = {"data":conversation}
#
#     if conversation:
#         return OK(data = conversation_data)
#     else:
#         raise NotFound()

@require_http_methods(["GET"])
def history(request):

    handler = Handler()
    id = ObjectId(request.META['HTTP_ID'])
    users = request.GET.getlist('user')

    temp = User.objects.get_one(queries={'_id': id}, projection={'friends': 1, '_id': 0})

    if not temp:
        raise NotFound()

    friends = temp['friends']
    if users:
        sorted_users = []
        for friend in friends:
            if str(friend) in users:
                sorted_users.append(str(friend))
        friends = sorted_users

    response = handler.getconversationhistory(str(id), friends)
    return OK(response)

@csrf_exempt
@require_http_methods(["PUT"])
def message(request):

    handler = Handler()
    sender = request.META['HTTP_ID']
    dest = json.loads(request.body.decode("utf-8"))
    msg = dest['data']
    broadcast = dest['broadcast']

    allusers =[str(user['_id']) for user in User.objects.get_all(projection={'_id':1})]

    if sender not in allusers:
        raise NotFound("Sender not found!")

    fname = User.objects.get_one(queries={'_id':ObjectId(sender)},projection={'_id':0,'fname':1})['fname']

    if broadcast == 0:
        receivers = dest['destination']
    else:
        receivers = [str(each['_id']) for each in User.objects.get_all(projection={'_id':1},queries={'_id':{'$ne':ObjectId(sender)}})]

    conversation_id = {}
    conversationIDs = []

    for receiver in receivers:
        if receiver not in allusers:
            raise NotFound("One of the recepient not found!")
        if sender < receiver:
            conv_id = sender + receiver
        else:
            conv_id = receiver + sender
        conversation_id[receiver] = conv_id
        conversationIDs.append(conv_id)

    latestchunk_id = Conversation.objects.get_all(queries={'id':{'$in':conversationIDs}},projection={'_id':0,'id':1,'chunks':{'$slice':[0,1]}})      #taking out latest chunk id

    chunk_mapping = {}
    for chunk in latestchunk_id:
        chunk_mapping[chunk['id']] = chunk['chunks'][0]

    handler.send_msg(sender,receivers,fname,msg,conversation_id,chunk_mapping)

    return OK({"Response":"Success!"})
