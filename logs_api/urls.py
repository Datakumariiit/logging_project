from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import DataChangeLogView

urlpatterns = [
  path('get-token/', obtain_auth_token, name='api_token_auth'),
  path('logs/<str:app_label>/<str:model_name>/<str:user>/', DataChangeLogView.as_view()),
]