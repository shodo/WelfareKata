from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from webapp.domain import UnitOfWork
from webapp.domain.services import AccountService, ProductService, PurchaseService
from webapp.repositories.django.django_unit_of_work import DjangoUnitOfWork
from webapp.repositories.sql_alchemy.sqlalchemy_unit_of_work import SqlAlchemyUnitOfWork


class ServiceLocator:
    session_factory = None

    def __init__(self, orm: str):
        self.orm = orm

    @staticmethod
    def _get_session_factory():
        path = __file__
        main_path = path.split("/welfarekata/webapp")[0]

        if ServiceLocator.session_factory is None:
            ServiceLocator.engine = create_engine(f"sqlite:///{main_path}/db.sqlite3")
            ServiceLocator.session_factory = sessionmaker()
            ServiceLocator.session_factory.configure(bind=ServiceLocator.engine)

        return ServiceLocator.session_factory

    def _get_unit_of_work(self) -> UnitOfWork:
        if self.orm == "sqlalchemy":
            return SqlAlchemyUnitOfWork(self._get_session_factory())
        else:
            return DjangoUnitOfWork()

    def account_service(self) -> AccountService:
        return AccountService(self._get_unit_of_work())

    def product_service(self) -> ProductService:
        return ProductService(self._get_unit_of_work())

    def purchase_service(self) -> PurchaseService:
        return PurchaseService(self._get_unit_of_work())


