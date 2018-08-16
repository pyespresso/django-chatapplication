"""infra URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from infra.controllers.info import info

urlpatterns = [
    path('accounts/<account_name>/info/', view=info, name='info'),
    path('',include('chats.urls')),
]

handler400 = 'infra.views.http_bad_request_view'
handler403 = 'infra.views.http_forbidden_view'
handler404 = 'infra.views.http_not_found_view'
handler500 = 'infra.views.http_server_error_view'
