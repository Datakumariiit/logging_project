from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import DataChangeLogView

urlpatterns = [
  path('get-token/', obtain_auth_token, name='api_token_auth'),
  path('logs/', DataChangeLogView.as_view()),
]