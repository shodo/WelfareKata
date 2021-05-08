from rest_framework import serializers
from rest_framework.serializers import Serializer

from welfarekata.webapp.serializers.responses.account_info_serializer import AccountInfoSerializer


class ProductSerializer(Serializer):

    id = serializers.UUIDField(allow_null=False, required=True)

    first_name = serializers.CharField(allow_null=False,
                                       required=True,
                                       max_length=100)

    last_name = serializers.CharField(allow_null=False,
                                      required=True,
                                      max_length=100)

    hiring_date = serializers.DateField(allow_null=False, required=True)

    account = AccountInfoSerializer(allow_null=False, required=True)
