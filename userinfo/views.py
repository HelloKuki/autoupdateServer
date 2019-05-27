# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sqlite3
import time

from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.compat import Serializer, PasswordField, get_username_field
from rest_framework_jwt.views import JSONWebTokenAPIView

from autoupdate import utils
from userinfo.Serializers import UserSerializers
from userinfo.models import User

from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER  # 生payload部分的方法
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER  # 生成jwt的方法

# class CustomBackend(ModelBackend):
#
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         try:
#             user = User.objects.get(Q(phone=username) & Q(password=password))
#             return user
#         except Exception as e:
#             return None
#
#
# def jwt_response_payload_handler(token, user=None, request=None):
#     return {
#         "code": 1000,
#         "msg": "登陆成功",
#         "token": token
#     }


class RegisterUser(APIView):

    def post(self, request, *args, **kwargs):

        msg = utils.verify(request, "phone", "password")

        phone = request.data.get("phone")
        password = request.data.get("password")

        if msg == "":
            msg = utils.verifyPhone(phone)
        if msg == "":
            msg = utils.verifyPassword(password)

        if not msg == "":
            result = {
                "code": 1002,
                "msg": msg
            }
            return JsonResponse(result, status=200)
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        query_sql = 'select * from userinfo_user where phone="%s"' % phone
        cursor.execute(query_sql)
        conn.commit()
        query_result = cursor.fetchall()
        if len(query_result) == 0 or query_result is None:
            token = utils.create_token(phone)
            create_time = time.time()
            sql = 'insert into userinfo_user (phone,password,nickname,create_time,token) values ("%s","%s","%s","%s",' \
                  '"%s")' % (phone, password, phone, create_time, token)
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            conn.close()
            result = {
                "code": 1000,
                "msg": "注册成功",
                "data": {
                    "token": token
                }
            }
            return JsonResponse(result, status=200)
        else:
            cursor.close()
            conn.close()
            result = {
                "code": 1001,
                "msg": "用户已存在"
            }
            return JsonResponse(result, status=200)


# class JSONWebTokenSerializer(Serializer):
#     """
#        Serializer class used to validate a username and password.
#
#        'username' is identified by the custom UserModel.USERNAME_FIELD.
#
#        Returns a JSON Web Token that can be used to authenticate later calls.
#        """
#
#     def __init__(self, *args, **kwargs):
#         """
#         Dynamically add the USERNAME_FIELD to self.fields.
#         """
#         super(JSONWebTokenSerializer, self).__init__(*args, **kwargs)
#
#         self.fields['phone'] = serializers.CharField()
#         self.fields['password'] = PasswordField(write_only=True)
#
#     @property
#     def username_field(self):
#         return get_username_field()
#
#     def validate(self, attrs):
#         credentials = {
#             'phone': attrs.get('phone'),
#             'password': attrs.get('password')
#         }
#
#         if all(credentials.values()):
#             user = authenticate(**credentials)
#
#             if user:
#                 if not user.is_active:
#                     msg = _('User account is disabled.')
#                     raise serializers.ValidationError(msg)
#
#                 payload = jwt_payload_handler(user)
#
#                 return {
#                     'token': jwt_encode_handler(payload),
#                     'user': user
#                 }
#             else:
#                 msg = _('Unable to log in with provided credentials.')
#                 raise serializers.ValidationError(msg)
#         else:
#             msg = _('Must include "phone" and "password".')
#             raise serializers.ValidationError(msg)


# class Login2(JSONWebTokenAPIView):
#     serializer_class = JSONWebTokenSerializer


class Login(APIView):

    def post(self, request, *args, **kwargs):
        msg = utils.verify(request, "phone", "password")

        phone = request.data.get("phone")
        password = request.data.get("password")

        if msg == "":
            msg = utils.verifyPhone(phone)
        if msg == "":
            msg = utils.verifyPassword(password)

        if not msg == "":
            result = {
                "code": 1002,
                "msg": msg
            }
            return JsonResponse(result, status=200)

        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        query_sql = 'select * from userinfo_user where phone="%s"' % phone
        cursor.execute(query_sql)
        conn.commit()
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        print user
        if user is None:
            result = {
                "code": 1002,
                "msg": "用户不存在"
            }
            return JsonResponse(result, status=200)

        if user[2] != password:
            result = {
                "code": 1002,
                "msg": "密码不正确"
            }
            return JsonResponse(result, status=200)

        userinfo = User()
        userinfo.__setattr__("phone", user[1] if not user[1] is None else "")
        userinfo.__setattr__("email", user[3] if not user[3] is None else "")
        userinfo.__setattr__("nickname", user[4] if not user[4] is None else "")
        userinfo.__setattr__("age", user[5] if not user[5] is None else -1)
        userinfo.__setattr__("token", user[6] if not user[6] is None else "")
        userinfo.__setattr__("create_time", user[7] if not user[7] is None else "")
        userinfo.__setattr__("update_time", user[8] if not user[8] is None else "")

        user_serializers = UserSerializers([userinfo], many=True)

        # payload = jwt_payload_handler(userinfo)  # 生成payload, 得到字典
        # token = jwt_encode_handler(payload)  # 生成jwt字符串
        result = {
            "code": 1000,
            "msg": "登陆成功",
            "data": user_serializers.data[0]
        }
        return JsonResponse(result, status=200)


class getUserInfo(APIView):
    authentication_classes = JSONWebTokenAuthentication

    def post(self, request, *args, **kwargs):

        msg = utils.verify(request, "token")
        if not msg == "":
            result = {
                "code": 1002,
                "msg": msg
            }
            return JsonResponse(result, status=200)

        token = request.data.get("token")

        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        query_sql = 'select * from userinfo_user where token="%s"' % token
        cursor.execute(query_sql)
        conn.commit()
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user is None:
            result = {
                "code": 1002,
                "msg": "token不正确"
            }
            return JsonResponse(result, status=200)

        userinfo = User()
        userinfo.__setattr__("phone", user[1] if not user[1] is None else "")
        userinfo.__setattr__("email", user[3] if not user[3] is None else "")
        userinfo.__setattr__("nickname", user[4] if not user[4] is None else "")
        userinfo.__setattr__("age", user[5] if not user[5] is None else -1)
        userinfo.__setattr__("token", user[6] if not user[6] is None else "")
        userinfo.__setattr__("create_time", user[7] if not user[7] is None else "")
        userinfo.__setattr__("update_time", user[8] if not user[8] is None else "")

        user_serializers = UserSerializers([userinfo], many=True)
        result = {
            "code": 1000,
            "msg": "请求成功",
            "data": user_serializers.data[0]
        }
        return JsonResponse(result, status=200)
