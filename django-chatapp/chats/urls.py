from django.contrib import admin
from django.urls import path , include
from chats.controllers.chat import users, message, history



urlpatterns = [
    path('admin/', admin.site.urls),
    path('users',view=users,name='users'),
    # path('conversation',view=conversation,name='convo'),
    # path('chunk',view=chunk,name='chunk'),
    path('message',view=message,name='send_msg'),
    path('history',view=history,name='history')
]
