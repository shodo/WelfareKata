from rest_framework import serializers
from rest_framework.serializers import Serializer


class ExternalIdSerializer(Serializer):
    id = serializers.UUIDField(allow_null=False, required=True)

    def to_internal_value(self, data):
        dict = {"id": data}
        return super().to_internal_value(dict)
