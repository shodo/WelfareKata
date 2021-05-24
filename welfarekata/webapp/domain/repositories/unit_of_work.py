import abc

from welfarekata.webapp.domain import AccountRepository, ProductRepository, PurchaseRepository


class UnitOfWork(abc.ABC):
    account_repository: AccountRepository
    product_repository: ProductRepository
    purchase_repository: PurchaseRepository

    def __enter__(self) -> 'UnitOfWork':
        return self

    def __exit__(self, *args):
        pass
