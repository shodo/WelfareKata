from django.db import transaction

from welfarekata.webapp.repositories.django_account_repository import DjangoAccountRepository
from welfarekata.webapp.repositories.django_product_repository import DjangoProductRepository
from welfarekata.webapp.repositories.django_purchase_repository import DjangoPurchaseRepository
from welfarekata.webapp.domain import UnitOfWork


class DjangoUnitOfWork(UnitOfWork):
    def __init__(self):
        self.atomic = transaction.atomic()

        self.account_repository = DjangoAccountRepository(self.atomic)
        self.product_repository = DjangoProductRepository(self.atomic)
        self.purchase_repository = DjangoPurchaseRepository(self.atomic)

    def __enter__(self):
        self.atomic.__enter__()
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.atomic.__exit__(*args)
