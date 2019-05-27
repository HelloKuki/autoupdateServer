from django.conf.urls import url
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token

from userinfo import views

urlpatterns = [
    url(r'^register', views.RegisterUser.as_view()),
    url(r'^login', views.Login.as_view()),
    url(r'^getUserInfo', views.getUserInfo.as_view()),
]
