from django.urls import path

from . import views

urlpatterns = [
    path('signup', views.UserSingUpView.as_view(), name='sign_up'),
    path('login', views.UserLoginView.as_view(), name='sign_up'),
    path('profile', views.UserRetrieveUpdateAPIView.as_view(), name='profile'),
    path('update_password', views.UserUpdatePasswordAPIView.as_view(), name='update_password'),
]
