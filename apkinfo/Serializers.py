from rest_framework import serializers

from apkinfo.models import ApkInfo, UpdateRecord


class ApkInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = ApkInfo()
        fields = ("_id", "app_name", "icon", "package_name", "app_key", "create_time", "update_time")


class UpdateRecordSerializers(serializers.ModelSerializer):
    class Meta:
        model = UpdateRecord()
        fields = ("app_id", "level", "package_name", "download_url", "version_code", "version_name", "min_sdk_version",
                  "target_sdk_version", "apk_size", "update_content", "update_type", "create_time", "app_name")
