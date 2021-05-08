from rest_framework import serializers
from rest_framework.serializers import Serializer


class AccountCreateSerializer(Serializer):
    employee_id = serializers.UUIDField(allow_null=False, required=True)
