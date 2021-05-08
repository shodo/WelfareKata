import uuid
from datetime import date
from typing import Optional, List
from welfarekata.webapp.exceptions import AccountNotFoundException, NoEnoughCreditsException, ProductNotFoundException
from welfarekata.webapp.services.pricing_service import PricingService
from welfarekata.webapp.models.purchase import Purchase
from welfarekata.webapp.dtos.purchase_dto import PurchaseDto
from welfarekata.webapp.models.product import Product

from django.db import transaction

from welfarekata.webapp.models import Account


class PurchaseService:
    @classmethod
    def get_purchase(cls, purchase_id: uuid.UUID) -> Optional[PurchaseDto]:
        try:
            purchase = Purchase.objects.get(external_id=purchase_id)
            return PurchaseDto.from_orm(purchase)
        except Account.DoesNotExist:
            return None

    @classmethod
    def create_purchase(
        cls,
        account_id: uuid.UUID,
        product_id: uuid.UUID,
    ) -> PurchaseDto:
        with transaction.atomic():
            try:
                account: Account = Account.objects.select_for_update().get(
                    external_id=account_id)

                product: Product = Product.objects.get(external_id=product_id)
            except Account.DoesNotExist:
                raise AccountNotFoundException()
            except Product.DoesNotExist:
                raise ProductNotFoundException()

            price = PricingService.calculate_price(product.type,
                                                   account.creation_date)

            if account.credits < price:
                raise NoEnoughCreditsException()

            account.credits -= price
            account.save()

            purchase = Purchase(account=account,
                                product=product,
                                spent_credits=price)
            purchase.save()

            return PurchaseDto.from_orm(purchase)

    @classmethod
    def list_purchases(cls) -> List[PurchaseDto]:
        purchases = Purchase.objects.all()
        return [PurchaseDto.from_orm(purchase) for purchase in purchases]
