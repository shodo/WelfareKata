from welfarekata.webapp.models.product import Product
from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_enumfield import EnumField


class ProductPartialUpdateSerializer(Serializer):
    name = serializers.CharField(allow_blank=True, allow_null=False, required=False, max_length=100)
    description = serializers.CharField(allow_blank=True, allow_null=False, required=False, max_length=100)
    type = EnumField(choices=Product.Type, allow_blank=True, allow_null=False, required=False)
