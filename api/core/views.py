from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
import rest_framework.status as status

from .models import User
from .serializers import UserSingUpSerializer, UserLoginSerializer


class UserSingUpView(CreateAPIView):
    serializer_class = UserSingUpSerializer
    queryset = User.objects.all()


# class UserLoginView(GenericAPIView):
#     serializer_class = UserLoginSerializer
#     queryset = User.objects.all()
#
#     def post(self, request, *args, **kwargs):
#         username = request.data['username']
#         password = request.data['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return Response(status=status.HTTP_200_OK)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
