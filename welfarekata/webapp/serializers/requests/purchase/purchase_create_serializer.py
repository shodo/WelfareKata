from rest_framework import serializers
from rest_framework.serializers import Serializer


class PurchaseCreateSerializer(Serializer):
    account_id = serializers.UUIDField(allow_null=False, required=True)
    product_id = serializers.UUIDField(allow_null=False, required=True)
