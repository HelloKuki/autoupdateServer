from django.conf.urls import url
from django.contrib import admin

from apkinfo import views

urlpatterns = [
    url(r'^createAppInfo', views.createAppInfo.as_view()),
    url(r'^uploadAppIcon', views.uploadAppIcon.as_view()),
    url(r'^uploadApkFile', views.uploadApkFile.as_view()),
    url(r'^explainApk', views.explainApk.as_view()),
    url(r'^releaseVersion', views.releaseVersion.as_view()),
    url(r'^checkUpdate', views.checkUpdate.as_view()),
]
