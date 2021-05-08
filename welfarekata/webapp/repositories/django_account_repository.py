import uuid
from typing import Optional, List

from welfarekata.webapp.domain.exceptions import AccountNotFoundException
from welfarekata.webapp import domain
from welfarekata.webapp import models as django_models


class DjangoAccountRepository:
    @classmethod
    def get(cls, account_id: uuid.UUID, for_update=False) -> Optional[domain.Account]:
        try:
            base_query = django_models.Account.objects

            if for_update:
                base_query = base_query.select_for_update()

            django_account = base_query.get(external_id=account_id)
            return cls._from_django_account_to_domain_account(django_account)

        except django_models.Account.DoesNotExist:
            return None

    @classmethod
    def list(cls, employee_id=None) -> List[domain.Account]:
        django_accounts = django_models.Account.objects

        if employee_id is not None:
            django_accounts = django_accounts.filter(employee_external_id=employee_id)

        return [cls._from_django_account_to_domain_account(django_account) for django_account in django_accounts.all()]

    @classmethod
    def add(cls, account: domain.Account) -> domain.Account:
        django_account = django_models.Account(
            external_id=account.id,
            employee_external_id=account.employee_id,
            creation_date=account.activation_date,
            credits=account.credits
        )
        django_account.save()

        return cls._from_django_account_to_domain_account(django_account)

    @classmethod
    def update(cls, account: domain.Account) -> domain.Account:
        try:
            django_account = django_models.Account.objects.get(external_id=account.id)
            django_account.employee_external_id = account.employee_id
            django_account.creation_date = account.activation_date
            django_account.credits = account.credits
            django_account.save()

            return cls._from_django_account_to_domain_account(django_account)
        except django_models.Account.DoesNotExist:
            raise AccountNotFoundException()

    @classmethod
    def _from_django_account_to_domain_account(cls, django_account: django_models.Account) -> domain.Account:
        return domain.Account(
            id=django_account.external_id,
            employee_id=django_account.employee_external_id,
            activation_date=django_account.creation_date,
            credits=django_account.credits
        )
