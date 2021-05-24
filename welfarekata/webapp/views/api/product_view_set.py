from welfarekata.webapp.repositories.django_unit_of_work import DjangoUnitOfWork
from welfarekata.webapp.repositories.django_product_repository import DjangoProductRepository
from welfarekata.webapp.serializers.requests.product import ProductCreateSerializer
from welfarekata.webapp.serializers.requests.product import ProductPartialUpdateSerializer
from welfarekata.webapp.serializers.requests import ExternalIdSerializer
from welfarekata.webapp.serializers.responses import ProductSerializer
from welfarekata.webapp.services import ProductService

from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet


class ProductViewSet(ViewSet):
    def retrieve(self, request, pk):
        serialized_id = ExternalIdSerializer(data=pk)

        if not serialized_id.is_valid():
            return Response(data=serialized_id.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        product_id = serialized_id.validated_data["id"]
        product_dto = ProductService(DjangoUnitOfWork()).get_product(product_id=product_id)

        if product_dto is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(
            data=ProductSerializer(product_dto).data,
            status=status.HTTP_200_OK,
        )

    def create(self, request):
        serialized_creation_request = ProductCreateSerializer(
            data=request.data)

        if not serialized_creation_request.is_valid():
            return Response(data=serialized_creation_request.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        validated_data = serialized_creation_request.validated_data
        product_dto = ProductService(DjangoUnitOfWork()).create_product(**validated_data)

        return Response(
            data=ProductSerializer(product_dto).data,
            status=status.HTTP_201_CREATED,
        )

    def list(self, request):
        product_dtos = ProductService(DjangoUnitOfWork()).list_products()

        return Response(
            data=[
                ProductSerializer(product_dto).data
                for product_dto in product_dtos
            ],
            status=status.HTTP_200_OK,
        )

    def partial_update(self, request, pk):
        serialized_id = ExternalIdSerializer(data=pk)

        if not serialized_id.is_valid():
            return Response(
                data=serialized_id.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        employee_id = serialized_id.validated_data["id"]

        serialized_partial_update_request = ProductPartialUpdateSerializer(
            data=request.data)

        if not serialized_partial_update_request.is_valid():
            return Response(data=serialized_partial_update_request.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        validated_data = serialized_partial_update_request.validated_data
        product_dto = ProductService(DjangoUnitOfWork()).update_product(employee_id, **validated_data)

        return Response(
            data=ProductSerializer(product_dto).data,
            status=status.HTTP_200_OK,
        )
