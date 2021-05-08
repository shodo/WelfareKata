import uuid
from datetime import datetime
from typing import Optional, List

from dateutil.tz import tz

from webapp.repositories.django_account_repository import DjangoAccountRepository
from webapp.repositories.django_product_repository import DjangoProductRepository
from webapp.repositories.django_purchase_repository import DjangoPurchaseRepository
from welfarekata.webapp.domain.exceptions import (
    NoEnoughCreditsException,
    ProductNotFoundException,
    AccountNotFoundException,
)
from welfarekata.webapp.services.pricing_service import PricingService
from welfarekata.webapp.domain.entities.purchase import Purchase
from welfarekata.webapp.dtos.purchase_dto import PurchaseDto
from django.db import transaction


class PurchaseService:
    @classmethod
    def get_purchase(cls, purchase_id: uuid.UUID) -> Optional[PurchaseDto]:
        purchase = DjangoPurchaseRepository.get(purchase_id)
        return PurchaseDto.from_entity(purchase) if purchase else None

    @classmethod
    def do_purchase(cls, account_id: uuid.UUID, product_id: uuid.UUID) -> PurchaseDto:
        with transaction.atomic():
            account = DjangoAccountRepository.get(account_id, for_update=True)
            if account is None:
                raise AccountNotFoundException()

            product = DjangoProductRepository.get(product_id)
            if product is None:
                raise ProductNotFoundException()

            price = PricingService.calculate_price(product.type, account.activation_date)

            if account.credits < price:
                raise NoEnoughCreditsException()

            account.credits -= price
            DjangoAccountRepository.update(account)

            purchase = Purchase(
                account_id=account_id,
                product_id=product_id,
                credits=price,
                creation_date=datetime.now(tz=tz.tzutc())
            )

            DjangoPurchaseRepository.add(purchase)

            return PurchaseDto.from_entity(purchase)

    @classmethod
    def list_purchases(cls) -> List[PurchaseDto]:
        purchases = DjangoPurchaseRepository.list()
        return [PurchaseDto.from_entity(purchase) for purchase in purchases]
