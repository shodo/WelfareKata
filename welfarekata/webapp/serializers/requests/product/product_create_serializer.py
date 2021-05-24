from welfarekata.webapp.orm_models.django.product import Product
from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_enumfield import EnumField


class ProductCreateSerializer(Serializer):
    name = serializers.CharField(allow_null=False, required=True, max_length=100)
    description = serializers.CharField(allow_null=False, required=True, max_length=100)
    type = EnumField(choices=Product.Type)
