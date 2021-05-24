from welfarekata.webapp.repositories.sql_alchemy.sqlalchemy_product_repository import SqlAlchemyProductRepository
from welfarekata.webapp.test.sql_alchemy_test_case import SqlAlchemyTestCase
from welfarekata.webapp import domain
from welfarekata.webapp.orm_models import sql_alchemy as sqla_models


class TestSqlAlchemyProductRepository(SqlAlchemyTestCase):
    def test_add(self):
        # Setup
        product = domain.Product(
            name="name",
            description="description",
            type=domain.Product.Type.BASIC,
        )

        session = self.session_factory()

        # SUT
        added_product = SqlAlchemyProductRepository(session).add(product)
        session.commit()

        orm_added_product = session.query(sqla_models.Product).one()

        # Asserts
        self.assertEqual(added_product, product)
        self.assertEqual(orm_added_product.external_id, added_product.id)
        self.assertEqual(orm_added_product.name, added_product.name)
        self.assertEqual(orm_added_product.description, added_product.description)
        self.assertEqual(orm_added_product.type, sqla_models.Product.Type(added_product.type.value).value)

    def test_get(self):
        # Setup
        session = self.session_factory()

        orm_product = sqla_models.Product(
            name="name",
            description="description",
            type=sqla_models.Product.Type.BASIC.value
        )
        session.add(orm_product)
        session.commit()

        # SUT
        retrieved_product = SqlAlchemyProductRepository(session).get(orm_product.external_id)

        # Asserts
        self.assertEqual(orm_product.external_id, retrieved_product.id)
        self.assertEqual(orm_product.name, retrieved_product.name)
        self.assertEqual(orm_product.description, retrieved_product.description)
        self.assertEqual(orm_product.type, sqla_models.Product.Type(retrieved_product.type.value).value)

    def test_list(self):
        # Setup
        session = self.session_factory()

        orm_product_one = sqla_models.Product(
            name="name1",
            description="description1",
            type=sqla_models.Product.Type.BASIC.value
        )
        session.add(orm_product_one)

        orm_product_two = sqla_models.Product(
            name="name2",
            description="description2",
            type=sqla_models.Product.Type.GOLD.value
        )
        session.add(orm_product_two)

        session.commit()

        # SUT
        retrieved_products = SqlAlchemyProductRepository(session).list()

        # Asserts
        retrieved_product_one = next(iter([product for product in retrieved_products
                                           if product.id == orm_product_one.external_id]), None)
        self.assertEqual(orm_product_one.external_id, retrieved_product_one.id)
        self.assertEqual(orm_product_one.name, retrieved_product_one.name)
        self.assertEqual(orm_product_one.description, retrieved_product_one.description)
        self.assertEqual(orm_product_one.type, sqla_models.Product.Type(retrieved_product_one.type.value).value)

        retrieved_product_two = next(iter([product for product in retrieved_products
                                           if product.id == orm_product_two.external_id]), None)
        self.assertEqual(orm_product_two.external_id, retrieved_product_two.id)
        self.assertEqual(orm_product_two.name, retrieved_product_two.name)
        self.assertEqual(orm_product_two.description, retrieved_product_two.description)
        self.assertEqual(orm_product_two.type, sqla_models.Product.Type(retrieved_product_two.type.value).value)

    def test_update(self):
        # Setup
        session = self.session_factory()

        orm_product = sqla_models.Product(
            name="name1",
            description="description1",
            type=sqla_models.Product.Type.BASIC.value
        )

        session.add(orm_product)
        session.commit()

        # SUT
        new_product = domain.Product(
            id=orm_product.external_id,
            name="updated_name",
            description="updated_description",
            type=domain.Product.Type.GOLD
        )
        updated_product = SqlAlchemyProductRepository(session).update(new_product)
        updated_orm_product = session.query(sqla_models.Product).one()

        # Asserts
        self.assertEqual(updated_product.id, new_product.id)
        self.assertEqual(updated_product.name, new_product.name)
        self.assertEqual(updated_product.description, new_product.description)
        self.assertEqual(updated_product.type, new_product.type)

        self.assertEqual(updated_orm_product.external_id, updated_product.id)
        self.assertEqual(updated_orm_product.name, updated_product.name)
        self.assertEqual(updated_orm_product.description, updated_product.description)
        self.assertEqual(updated_orm_product.type, sqla_models.Product.Type(updated_product.type.value).value)
