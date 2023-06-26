from django.urls import path

from . import views

urlpatterns = [
    path('signup', views.UserSingUpView.as_view(), name='sign_up'),
    path('login', views.UserLoginView.as_view(), name='sign_up'),
]