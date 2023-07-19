from django.urls import path
from .views import BotVerifyAPIView

urlpatterns = [
    path('verify', BotVerifyAPIView.as_view(), name='bot_verify'),
]
