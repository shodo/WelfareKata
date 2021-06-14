from webapp.repositories.sql_alchemy.session_factory import ServiceLocator
from webapp.repositories.sql_alchemy.sqlalchemy_unit_of_work import SqlAlchemyUnitOfWork
from welfarekata.webapp.repositories.django.django_unit_of_work import DjangoUnitOfWork
from welfarekata.webapp.domain.exceptions import AccountAlreadyActivatedException
from welfarekata.webapp.serializers.requests.account.account_create_serializer import AccountCreateSerializer
from welfarekata.webapp.serializers.responses.account_info_serializer import AccountSerializer
from welfarekata.webapp.domain.services import AccountService
from welfarekata.webapp.serializers.requests import ExternalIdSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet


class AccountViewSet(ViewSet):
    def retrieve(self, request, pk):
        serialized_id = ExternalIdSerializer(data=pk)

        if not serialized_id.is_valid():
            return Response(data=serialized_id.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        account_id = serialized_id.validated_data["id"]
        orm = request.query_params.get('orm', None)
        account_service = ServiceLocator(orm).account_service()
        account_dto = account_service.get_account(account_id=account_id)

        if account_dto is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(
            data=AccountSerializer(account_dto).data,
            status=status.HTTP_200_OK,
        )

    def create(self, request):
        serialized_creation_request = AccountCreateSerializer(
            data=request.data)

        if not serialized_creation_request.is_valid():
            return Response(data=serialized_creation_request.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        validated_data = serialized_creation_request.validated_data

        try:
            orm = request.query_params.get('orm', None)
            account_service = ServiceLocator(orm).account_service()
            account_dto = account_service.activate_account(**validated_data)

            return Response(
                data=AccountSerializer(account_dto).data,
                status=status.HTTP_201_CREATED,
            )
        except AccountAlreadyActivatedException:
            return Response(
                data={"message": "Account already activated"},
                status=status.HTTP_409_CONFLICT
            )

    def list(self, request):
        orm = request.query_params.get('orm', None)
        account_service = ServiceLocator(orm).account_service()
        account_dtos = account_service.list_accounts()

        return Response(
            data=[
                AccountSerializer(account_dto).data for account_dto in account_dtos
            ],
            status=status.HTTP_200_OK,
        )
