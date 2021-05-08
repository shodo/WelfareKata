from rest_framework import serializers
from rest_framework.serializers import Serializer


class PurchaseSerializer(Serializer):
    id = serializers.UUIDField(allow_null=False, required=True)
    account_id = serializers.UUIDField(allow_null=False, required=True)
    product_id = serializers.UUIDField(allow_null=False, required=True)
    credits = serializers.IntegerField(allow_null=False, required=True)
