from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings

from .serializer import BotVerifySerializer
from .models import TelegramUser
from .tg.client import TgClient


class BotVerifyAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BotVerifySerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        verification_code = serializer.data['verification_code']
        try:
            tg_user = TelegramUser.objects.get(verification_code=verification_code)
        except TelegramUser.DoesNotExist:
            return Response({'verification_code': ['Bad verification code']}, status=status.HTTP_400_BAD_REQUEST)

        if tg_user.user is not None:
            return Response({'verification_code': ['You have already connected the bot']},
                            status=status.HTTP_400_BAD_REQUEST)

        tg_user.user = self.request.user
        tg_user.position = TelegramUser.Position.wait_command
        tg_user.save()

        message = 'Вы успешно подключились к приложению!'
        TgClient().send_message(tg_user.tg_chat_id, message)

        return Response(status=status.HTTP_200_OK)
