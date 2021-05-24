from django.db import transaction

from webapp.domain import UnitOfWork


class DjangoUnitOfWork(UnitOfWork):
    def __init__(self):
        self.atomic = transaction.atomic()

    def __enter__(self):
        self.atomic.__enter__()
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.atomic.__exit__(*args)
