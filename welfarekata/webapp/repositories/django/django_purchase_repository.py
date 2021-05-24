import uuid
from typing import Optional, List

from django.db import transaction

from welfarekata.webapp.domain import PurchaseRepository
from welfarekata.webapp import domain
from welfarekata.webapp.orm_models import django as django_models
from welfarekata.webapp.domain.exceptions import AccountNotFoundException, ProductNotFoundException


class DjangoPurchaseRepository(PurchaseRepository):
    def __init__(self, atomic: transaction.Atomic):
        self.atomic = atomic

    def get(self, purchase_id: uuid.UUID) -> Optional[domain.Purchase]:
        try:
            django_purchase = django_models.Purchase.objects.get(external_id=purchase_id)
            return self._from_django_purchase_to_domain_purchase(django_purchase)

        except django_models.Purchase.DoesNotExist:
            return None

    def list(self) -> List[domain.Purchase]:
        django_purchases = django_models.Purchase.objects.all()
        return [self._from_django_purchase_to_domain_purchase(django_purchase) for django_purchase in django_purchases]

    def add(self, purchase: domain.Purchase) -> domain.Purchase:
        try:
            django_account = django_models.Account.objects.get(external_id=purchase.account_id)
        except django_models.Account.DoesNotExist:
            raise AccountNotFoundException()

        try:
            django_product = django_models.Product.objects.get(external_id=purchase.product_id)
        except django_models.Product.DoesNotExist:
            raise ProductNotFoundException()

        django_purchase = django_models.Purchase(
            external_id=purchase.id,
            account=django_account,
            product=django_product,
            spent_credits=purchase.credits,
            creation_date=purchase.creation_date
        )
        django_purchase.save()

        return self._from_django_purchase_to_domain_purchase(django_purchase)

    @classmethod
    def _from_django_purchase_to_domain_purchase(cls, django_purchase: django_models.Purchase) -> domain.Purchase:
        return domain.Purchase(
            id=django_purchase.external_id,
            account_id=django_purchase.account.external_id,
            product_id=django_purchase.product.external_id,
            credits=django_purchase.spent_credits,
            creation_date=django_purchase.creation_date
        )
