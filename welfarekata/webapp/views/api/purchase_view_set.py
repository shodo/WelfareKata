from welfarekata.webapp.repositories.django.django_unit_of_work import DjangoUnitOfWork
from welfarekata.webapp.domain.exceptions import NoEnoughCreditsException
from welfarekata.webapp.serializers.requests.purchase.purchase_create_serializer import PurchaseCreateSerializer
from welfarekata.webapp.serializers.responses.purchase_serializer import PurchaseSerializer
from welfarekata.webapp.domain.services import PurchaseService
from welfarekata.webapp.serializers.requests import ExternalIdSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet


class PurchaseViewSet(ViewSet):
    def retrieve(self, request, pk):
        serialized_id = ExternalIdSerializer(data=pk)

        if not serialized_id.is_valid():
            return Response(data=serialized_id.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        purchase_id = serialized_id.validated_data["id"]
        purchase_dto = PurchaseService(DjangoUnitOfWork()).get_purchase(purchase_id=purchase_id)

        if purchase_dto is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(data=PurchaseSerializer(purchase_dto).data, status=status.HTTP_200_OK)

    def create(self, request):
        serialized_creation_request = PurchaseCreateSerializer(
            data=request.data)

        if not serialized_creation_request.is_valid():
            return Response(data=serialized_creation_request.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        validated_data = serialized_creation_request.validated_data

        try:
            purchase_dto = PurchaseService(DjangoUnitOfWork()).do_purchase(**validated_data)

            return Response(data=PurchaseSerializer(purchase_dto).data, status=status.HTTP_201_CREATED)
        except NoEnoughCreditsException:
            return Response(data={"message": "No enough credits for this purchase"}, status=status.HTTP_409_CONFLICT)

    def list(self, request):
        purchase_dtos = PurchaseService(DjangoUnitOfWork()).list_purchases()

        return Response(
            data=[
                PurchaseSerializer(purchase_dto).data
                for purchase_dto in purchase_dtos
            ],
            status=status.HTTP_200_OK,
        )
