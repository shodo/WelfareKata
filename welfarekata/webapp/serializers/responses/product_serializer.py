from rest_enumfield import EnumField
from rest_framework import serializers
from rest_framework.serializers import Serializer

from welfarekata.webapp.dtos import ProductDto


class ProductSerializer(Serializer):
    id = serializers.UUIDField(allow_null=False, required=True)
    name = serializers.CharField(allow_null=False, required=True, max_length=100)
    description = serializers.CharField(allow_null=False, required=True, max_length=100)
    type = EnumField(choices=ProductDto.Type)

