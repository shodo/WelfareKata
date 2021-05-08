from rest_framework import serializers
from rest_framework.serializers import Serializer


class AccountSerializer(Serializer):
    id = serializers.UUIDField(allow_null=False, required=True)
    credits = serializers.IntegerField(allow_null=False, required=True)
    employee_id = serializers.UUIDField(allow_null=False, required=True)
    activation_date = serializers.DateField(allow_null=False, required=True)
