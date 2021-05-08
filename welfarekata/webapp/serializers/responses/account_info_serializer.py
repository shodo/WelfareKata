from rest_framework import serializers
from rest_framework.serializers import Serializer


class AccountInfoSerializer(Serializer):

    id = serializers.UUIDField(allow_null=False, required=True)

    credits = serializers.IntegerField(allow_null=False, required=True)
