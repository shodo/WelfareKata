import uuid
from datetime import datetime
from typing import Optional, List

from dateutil import tz

from welfarekata.webapp.domain import UnitOfWork
from welfarekata.webapp.domain import Purchase
from welfarekata.webapp.domain.exceptions import NoEnoughCreditsException
from welfarekata.webapp.domain.exceptions import AccountNotFoundException, ProductNotFoundException
from welfarekata.webapp.domain.services.pricing_service import PricingService
from welfarekata.webapp.dtos.purchase_dto import PurchaseDto


class PurchaseService:
    def __init__(self, unit_of_work: UnitOfWork):
        self.uow = unit_of_work

    def get_purchase(self, purchase_id: uuid.UUID) -> Optional[PurchaseDto]:
        purchase = self.uow.purchase_repository.get(purchase_id)
        return PurchaseDto.from_entity(purchase) if purchase else None

    def do_purchase(self, account_id: uuid.UUID, product_id: uuid.UUID) -> PurchaseDto:
        with self.uow:
            account = self.uow.account_repository.get(account_id, for_update=True)
            if account is None:
                raise AccountNotFoundException()

            product = self.uow.product_repository.get(product_id)
            if product is None:
                raise ProductNotFoundException()

            price = PricingService.calculate_price(product.type, account.activation_date)

            if account.credits < price:
                raise NoEnoughCreditsException()

            account.credits -= price
            self.uow.account_repository.update(account)

            purchase = Purchase(
                account_id=account_id,
                product_id=product_id,
                credits=price,
                creation_date=datetime.now(tz=tz.tzutc())
            )

            self.uow.purchase_repository.add(purchase)

            return PurchaseDto.from_entity(purchase)

    def list_purchases(self) -> List[PurchaseDto]:
        purchases = self.uow.purchase_repository.list()
        return [PurchaseDto.from_entity(purchase) for purchase in purchases]
