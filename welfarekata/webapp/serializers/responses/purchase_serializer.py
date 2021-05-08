from rest_framework import serializers
from rest_framework.serializers import Serializer

from welfarekata.webapp.serializers.responses.account_info_serializer import AccountInfoSerializer


class PurchaseSerializer(Serializer):
    id = serializers.UUIDField(allow_null=False, required=True)
    account_id = serializers.UUIDField(allow_null=False, required=True)
    product_id = serializers.UUIDField(allow_null=False, required=True)
    credits = serializers.IntegerField(allow_null=False, required=True)
