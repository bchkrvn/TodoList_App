from django.contrib.auth import authenticate, login, logout
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import rest_framework.status as status
from rest_framework.views import APIView

from .models import User
from .serializers import UserSingUpSerializer, UserSerializer, UserChangePasswordSerializer


class UserSingUpView(CreateAPIView):
    serializer_class = UserSingUpSerializer
    queryset = User.objects.all()


class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserUpdatePasswordAPIView(UpdateAPIView):
    serializer_class = UserChangePasswordSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
