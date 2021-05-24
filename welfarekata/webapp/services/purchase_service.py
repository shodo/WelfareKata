import uuid
from datetime import datetime
from typing import Optional, List

from dateutil import tz

from welfarekata.webapp.domain import UnitOfWork
from welfarekata.webapp.domain import Purchase, PurchaseRepository, AccountRepository, ProductRepository
from welfarekata.webapp.domain.exceptions import NoEnoughCreditsException
from welfarekata.webapp.domain.exceptions import AccountNotFoundException, ProductNotFoundException
from welfarekata.webapp.services.pricing_service import PricingService
from welfarekata.webapp.dtos.purchase_dto import PurchaseDto


class PurchaseService:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
        purchase_repository: PurchaseRepository,
        product_repository: ProductRepository,
        account_repository: AccountRepository
    ):
        self.uow = unit_of_work
        self.purchase_repository = purchase_repository
        self.product_repository = product_repository
        self.account_repository = account_repository

    def get_purchase(self, purchase_id: uuid.UUID) -> Optional[PurchaseDto]:
        purchase = self.purchase_repository.get(purchase_id)
        return PurchaseDto.from_entity(purchase) if purchase else None

    def do_purchase(self, account_id: uuid.UUID, product_id: uuid.UUID) -> PurchaseDto:
        with self.uow:
            account = self.account_repository.get(account_id, for_update=True)
            if account is None:
                raise AccountNotFoundException()

            product = self.product_repository.get(product_id)
            if product is None:
                raise ProductNotFoundException()

            price = PricingService.calculate_price(product.type, account.activation_date)

            if account.credits < price:
                raise NoEnoughCreditsException()

            account.credits -= price
            self.account_repository.update(account)

            purchase = Purchase(
                account_id=account_id,
                product_id=product_id,
                credits=price,
                creation_date=datetime.now(tz=tz.tzutc())
            )

            self.purchase_repository.add(purchase)

            return PurchaseDto.from_entity(purchase)

    def list_purchases(self) -> List[PurchaseDto]:
        purchases = self.purchase_repository.list()
        return [PurchaseDto.from_entity(purchase) for purchase in purchases]
