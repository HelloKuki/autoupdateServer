# -*- coding: utf-8 -*-


import base64
import os
import re
import sqlite3
import time
from django.http import JsonResponse
from rest_framework.views import APIView
from apkinfo.Serializers import ApkInfoSerializers, UpdateRecordSerializers
from apkinfo.models import ApkInfo, UpdateRecord
from autoupdate import utils
import subprocess


class createAppInfo(APIView):

    def __init__(self, **kwargs):
        super(createAppInfo, self).__init__(**kwargs)
        self.conn = sqlite3.connect("db.sqlite3")
        self.cursor = self.conn.cursor()

    def post(self, request, *args, **kwargs):
        msg = utils.verify(request, "token", "app_name", "package_name")
        if not msg == "":
            return self.returnError(1002, msg)

        token = request.data.get("token")

        query_sql = 'select * from userinfo_user where token="%s"' % token
        self.cursor.execute(query_sql)
        self.conn.commit()
        user = self.cursor.fetchone()

        if user is None or not user[6] == token:
            return self.returnError(1003, "token不正确")
        user_id = user[0]
        app_name = request.data.get("app_name")
        package_name = request.data.get("package_name")

        if len(app_name) > 20:
            return self.returnError(1004, "应用名长度不能超过20")

        if package_name.find(".") == -1:
            return self.returnError(1005, "请输入合法包名")

        query_app_sql = 'select * from apkinfo_apkinfo where package_name="%s"' % package_name
        self.cursor.execute(query_app_sql)
        self.conn.commit()
        app_info = self.cursor.fetchone()
        if not app_info is None:
            return self.returnError("1006", "包名已被使用")

        app_key = base64.b64encode(package_name)
        if len(app_key) < 32:
            s = utils.create_random(32 - len(app_key))
            app_key = app_key + s
        elif len(app_key) > 32:
            app_key = app_key[0:32]

        insert_sql = 'insert into apkinfo_apkinfo (app_name,package_name,app_key,create_time) values ("%s","%s","%s",' \
                     '"%s")' % (app_name, package_name, app_key, time.time())

        self.cursor.execute(insert_sql)
        self.conn.commit()

        query_app_sql = 'select * from apkinfo_apkinfo where package_name="%s"' % package_name
        self.cursor.execute(query_app_sql)
        self.conn.commit()
        app_info = self.cursor.fetchone()

        if app_info is None:
            return self.returnError(1007, "创建失败")

        user_bind_app_sql = 'insert into user_to_apkinfo (userid,apkinfoid) values ("%s","%s")' % (user_id, app_info[0])
        self.cursor.execute(user_bind_app_sql)
        self.conn.commit()

        apkinfo = ApkInfo()
        apkinfo.__setattr__("_id", app_info[0])
        apkinfo.__setattr__("app_name", app_info[1])
        apkinfo.__setattr__("package_name", app_info[3])
        apkinfo.__setattr__("app_key", app_info[4])
        apkinfo.__setattr__("create_time", app_info[5])

        apkinfo_data = ApkInfoSerializers([apkinfo], many=True)

        self.cursor.close()
        self.conn.close()
        result = {
            "code": 1000,
            "msg": "创建成功",
            "data": apkinfo_data.data[0]
        }
        return JsonResponse(result, status=200)

    def returnError(self, error_code, msg):
        if not self.cursor is None:
            self.cursor.close()
            self.conn.close()
        result = {
            "code": error_code,
            "msg": msg
        }
        return JsonResponse(result, status=200)


class uploadAppIcon(APIView):

    def post(self, request, *args, **kwargs):
        img = request.FILES.get('img')
        print img.name
        print img.size
        return JsonResponse({"code": 1000}, status=200)


class uploadApkFile(APIView):

    def post(self, request, *args, **kwargs):
        app_id = request.data.get("app_id")
        apk_file = request.FILES.get('apk_file')
        file_path = "./static/apk/%s" % apk_file.name
        f = open(file_path, "wb")
        for i in apk_file.chunks():
            f.write(i)
        f.close()
        download_url = "http://%s/static/apk/%s" % (request.get_host(), apk_file.name)
        apk_size = os.path.getsize(file_path)
        result = {
            "code": 1000,
            "msg": "上传成功",
            "data": {
                "path": file_path,
                "apk_size": apk_size,
                "download_url": download_url
            }
        }
        return JsonResponse(result, status=200)


class explainApk(APIView):

    def __init__(self):
        self.aapt_path = r"E:\python\workspace\autoupdate\tool\aapt.exe"

    def post(self, request, *args, **kwargs):
        apk_path = request.data.get("file_path")
        # apk_path="./static/apk/android-1.2.7.apk"
        print apk_path
        cmd = self.aapt_path + " dump badging %s" % apk_path
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        package_name = re.compile("'(.*?)'").search(re.compile("package: name='(\S+)'").search(output).group(0)).group(
            0)[1:-1]
        version_code = re.compile("'(.*?)'").search(re.compile("versionCode='(\S+)'").search(output).group(0)).group(0)[
                       1:-1]
        version_name = re.compile("'(.*?)'").search(re.compile("versionName='(\S+)'").search(output).group(0)).group(0)[
                       1:-1]
        min_sdk_version = re.compile("'(.*?)'").search(re.compile("sdkVersion:'(\S+)'").search(output).group(0)).group(
            0)[1:-1]
        target_sdk_version = re.compile("'(.*?)'").search(
            re.compile("targetSdkVersion:'(\S+)'").search(output).group(0)).group(0)[1:-1]
        app_name = re.compile("'(.*?)'").search(re.compile("application-label:'(\S+)'").search(output).group(0)).group(
            0)[1:-1]

        result = {
            "code": 1000,
            "msg": "请求成功",
            "data": {
                "package_name": package_name,
                "version_code": version_code,
                "version_name": version_name,
                "min_sdk_version": min_sdk_version,
                "target_sdk_version": target_sdk_version,
                "app_name": app_name,
            }
        }
        return JsonResponse(result, status=200)


# 发布更新
class releaseVersion(APIView):

    def __init__(self, **kwargs):
        super(releaseVersion, self).__init__(**kwargs)
        self.conn = sqlite3.connect("db.sqlite3")
        self.cursor = self.conn.cursor()

    def post(self, request, *args, **kwargs):
        msg = utils.verify(request, "app_id", "app_name", "package_name", "version_code", "version_name",
                           "min_sdk_version", "target_sdk_version", "app_name", "update_type", "download_url",
                           "apk_size")
        if not msg == "":
            return self.returnError(1002, msg)

        app_id = request.data.get("app_id")
        package_name = request.data.get("package_name")
        version_code = request.data.get("version_code")
        version_name = request.data.get("version_name")
        min_sdk_version = request.data.get("min_sdk_version")
        target_sdk_version = request.data.get("target_sdk_version")
        app_name = request.data.get("app_name")
        update_type = request.data.get("update_type")
        update_content = request.data.get("update_content")
        download_url = request.data.get("download_url")
        apk_size = request.data.get("apk_size")
        create_time = time.time()

        query_sql = 'SELECT MAX(level) FROM apkinfo_updaterecord WHERE app_id = %s' % app_id

        self.cursor.execute(query_sql)
        self.conn.commit()
        level_result = self.cursor.fetchone()
        if level_result[0] is None:
            level = 1
        else:
            level = level_result[0] + 1

        insert_sql = 'insert into apkinfo_updaterecord (app_id,level,package_name,download_url,version_code,' \
                     'version_name,min_sdk_version,target_sdk_version,apk_size,update_content,update_type,' \
                     'create_time,app_name) values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
                         app_id, level, package_name, download_url, version_code, version_name, min_sdk_version,
                         target_sdk_version, apk_size, update_content, update_type, create_time, app_name)

        self.cursor.execute(insert_sql)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        result = {
            "code": 1000,
            "msg": "发布成功"
        }
        return JsonResponse(result, status=200)

    def returnError(self, error_code, msg):
        if not self.cursor is None:
            self.cursor.close()
            self.conn.close()
        result = {
            "code": error_code,
            "msg": msg
        }
        return JsonResponse(result, status=200)


# 检测更新
class checkUpdate(APIView):

    def __init__(self, **kwargs):
        super(checkUpdate, self).__init__(**kwargs)
        self.conn = sqlite3.connect("db.sqlite3")
        self.cursor = self.conn.cursor()

    def post(self, request, *args, **kwargs):

        msg = utils.verify(request, "app_key")
        if not msg == "":
            return self.returnError(1002, msg)
        key = request.data.get("app_key")
        query_sql = 'select * from apkinfo_apkinfo where app_key = "%s"' % key

        self.cursor.execute(query_sql)
        self.conn.commit()
        app_info = self.cursor.fetchone()
        if app_info is None:
            return self.returnError(1003, "App信息为null")
        app_id = app_info[0]

        query_update_sql = 'SELECT * FROM apkinfo_updaterecord WHERE app_id = "%s" ORDER BY level DESC LIMIT 1' % app_id
        self.cursor.execute(query_update_sql)
        self.conn.commit()

        apk_record = self.cursor.fetchone()
        print apk_record
        if apk_record is None:
            return self.returnError(1003, "更新数据为null")

        self.cursor.close()
        self.conn.close()
        result = {
            "code": 1000,
            "msg": "请求成功",
            "data": {
                "app_id": apk_record[1],
                "level": apk_record[2],
                "package_name": apk_record[3],
                "download_url": apk_record[4],
                "version_code": apk_record[5],
                "version_name": apk_record[6],
                "min_sdk_version": apk_record[7],
                "target_sdk_version": apk_record[8],
                "apk_size": apk_record[9],
                "update_content": apk_record[10] if not apk_record[10] is None and not apk_record[10] == "None" else "",
                "update_type": apk_record[11],
                "create_time": apk_record[12],
                "app_name": apk_record[13],
                "progress_notify_type": app_info[7],
            }
        }
        return JsonResponse(result, status=200)

    def returnError(self, error_code, msg):
        if not self.cursor is None:
            self.cursor.close()
            self.conn.close()
        result = {
            "code": error_code,
            "msg": msg
        }
        return JsonResponse(result, status=200)
