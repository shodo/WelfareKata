import uuid
from typing import Optional, List

import sqlalchemy
from sqlalchemy.orm import Session

from welfarekata.webapp.domain import PurchaseRepository
from welfarekata.webapp import domain
from welfarekata.webapp.orm_models import sql_alchemy as sqla_models
from welfarekata.webapp.domain.exceptions import AccountNotFoundException, ProductNotFoundException


class SqlAlchemyPurchaseRepository(PurchaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def get(self, purchase_id: uuid.UUID) -> Optional[domain.Purchase]:
        pass
        try:
            sqla_purchase = self.session.query(sqla_models.Purchase).filter(
                sqla_models.Purchase.external_id == purchase_id
            ).one()

            return self._from_sqla_purchase_to_domain_purchase(sqla_purchase)

        except sqlalchemy.orm.exc.NoResultFound:
            return None

    def list(self) -> List[domain.Purchase]:
        sqla_purchases = self.session.query(sqla_models.Purchase)
        return [self._from_sqla_purchase_to_domain_purchase(sqla_purchase) for sqla_purchase in sqla_purchases]

    def add(self, purchase: domain.Purchase) -> domain.Purchase:
        try:
            sqla_account = self.session.query(sqla_models.Account).filter(
                sqla_models.Account.external_id == purchase.account_id
            ).one()
        except sqlalchemy.orm.exc.NoResultFound:
            raise AccountNotFoundException()

        try:
            sqla_product = self.session.query(sqla_models.Product).filter(
                sqla_models.Product.external_id == purchase.product_id
            ).one()
        except sqlalchemy.orm.exc.NoResultFound:
            raise ProductNotFoundException()

        sqla_purchase = sqla_models.Purchase(
            external_id=purchase.id,
            account=sqla_account,
            product=sqla_product,
            spent_credits=purchase.credits,
            creation_date=purchase.creation_date
        )
        self.session.add(sqla_purchase)

        return self._from_sqla_purchase_to_domain_purchase(sqla_purchase)

    @classmethod
    def _from_sqla_purchase_to_domain_purchase(cls, sqla_purchase: sqla_models.Purchase) -> domain.Purchase:
        return domain.Purchase(
            id=sqla_purchase.external_id,
            account_id=sqla_purchase.account.external_id,
            product_id=sqla_purchase.product.external_id,
            credits=sqla_purchase.spent_credits,
            creation_date=sqla_purchase.creation_date
        )
