import uuid
from typing import Optional, List

import sqlalchemy
from sqlalchemy.orm import Session

import welfarekata.webapp.orm_models.sql_alchemy as sqla_models
from welfarekata.webapp.domain import ProductRepository
from welfarekata.webapp import domain
from welfarekata.webapp.domain.exceptions import ProductNotFoundException


class SqlAlchemyProductRepository(ProductRepository):
    def __init__(self, session: Session):
        self.session = session

    def get(self, product_id: uuid.UUID) -> Optional[domain.Product]:
        try:
            sqla_product = self.session.query(sqla_models.Product).filter(
                sqla_models.Product.external_id == product_id).one()

            return self._from_sql_alchemy_product_to_domain_product(sqla_product)

        except sqlalchemy.orm.exc.NoResultFound:
            return None

    def list(self) -> List[domain.Product]:
        sqla_products = self.session.query(sqla_models.Product)
        return [self._from_sql_alchemy_product_to_domain_product(sqla_product) for sqla_product in sqla_products]

    def add(self, product: domain.Product) -> domain.Product:
        sqla_product = sqla_models.Product(
            external_id=product.id,
            name=product.name,
            description=product.description,
            type=sqla_models.Product.Type(product.type.value).value
        )
        self.session.add(sqla_product)

        return self._from_sql_alchemy_product_to_domain_product(sqla_product)

    def update(self, product: domain.Product) -> domain.Product:
        self.session.begin_nested()

        try:
            sqla_product = self.session.query(sqla_models.Product).filter(
                sqla_models.Product.external_id == product.id).one()

        except sqlalchemy.orm.exc.NoResultFound:
            self.session.rollback()
            raise ProductNotFoundException()

        sqla_product.name = product.name
        sqla_product.description = product.description
        sqla_product.type = sqla_models.Product.Type(product.type.value).value
        self.session.commit()

        return self._from_sql_alchemy_product_to_domain_product(sqla_product)

    @classmethod
    def _from_sql_alchemy_product_to_domain_product(cls, sqla_product: sqla_models.Product) -> domain.Product:
        return domain.Product(
            id=sqla_product.external_id,
            name=sqla_product.name,
            description=sqla_product.description,
            type=domain.Product.Type(sqla_product.type)
        )