from sqlalchemy.orm import sessionmaker

from welfarekata.webapp.repositories.sql_alchemy.sqlalchemy_account_repository import SqlAlchemyAccountRepository
from welfarekata.webapp.repositories.sql_alchemy.sqlalchemy_product_repository import SqlAlchemyProductRepository
from welfarekata.webapp.repositories.sql_alchemy.sqlalchemy_purchase_repository import SqlAlchemyPurchaseRepository
from welfarekata.webapp.domain import UnitOfWork


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: sessionmaker):
        self.session = session_factory()
        self.ref_count = 0

        self.account_repository = SqlAlchemyAccountRepository(self.session)
        self.product_repository = SqlAlchemyProductRepository(self.session)
        self.purchase_repository = SqlAlchemyPurchaseRepository(self.session)

    def __enter__(self):
        if self.ref_count > 0:
            self.session.begin_nested()

        self.ref_count += 1

        return super().__enter__()

    def __exit__(self, exc_type, exc_value, traceback):
        self.ref_count -= 1

        exception_occurred = exc_type is not None
        if not exception_occurred:
            self.session.commit()
        else:
            self.session.rollback()

        if self.ref_count == 0:
            self.session.close()

        super().__exit__(exc_type, exc_value, traceback)
