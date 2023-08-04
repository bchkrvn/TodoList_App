from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializer import BotVerifySerializer
from .models import TelegramUser
from .tg.client import TgClient
from .tg.tasks import send_email_task


class BotVerifyAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BotVerifySerializer

    @extend_schema(request=BotVerifySerializer,
                   description='Connect todolist with telegram bot', summary='Connect with tg bot',
                   responses={200: OpenApiResponse(description='Successful connect'),
                              400: OpenApiResponse(description='Wrong verification code')})
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
        TgClient().create_and_send_message(tg_user.tg_chat_id, message)

        if tg_user.user.email:
            send_email_task.delay(tg_user.user_id)

        return Response(status=status.HTTP_200_OK)
