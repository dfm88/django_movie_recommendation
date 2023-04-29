from common.serializers import BaseMeta
from rest_framework import serializers
from user.models import UserCustom


class InputUserSerializer(serializers.ModelSerializer):
    class Meta(BaseMeta):
        model = UserCustom
        exclude = ("last_login",)


class OutputUserSerializer(serializers.ModelSerializer):
    class Meta(BaseMeta):
        model = UserCustom
        exclude = (
            "groups",
            "user_permissions",
            "last_login",
        )
        extra_kwargs = {'password': {'write_only': True}}


class OutputUserSerializerLight(serializers.ModelSerializer):
    class Meta:
        model = UserCustom
        fields = ("id", "username")
