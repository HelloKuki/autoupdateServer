from rest_framework import serializers

from userinfo.models import User


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User()
        fields = ("phone", "email", "nickname", "age", "token", "create_time", "update_time")
