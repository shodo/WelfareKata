import uuid
from typing import Optional, List

import sqlalchemy
from sqlalchemy.orm import Session
import welfarekata.webapp.orm_models.sql_alchemy as sqla_models
from welfarekata.webapp.domain.exceptions import AccountNotFoundException
from welfarekata.webapp import domain
from welfarekata.webapp.domain import AccountRepository


class SqlAlchemyAccountRepository(AccountRepository):
    def __init__(self, session: Session):
        self.session = session

    def get(self, account_id: uuid.UUID, for_update=False) -> Optional[domain.Account]:
        try:
            base_query = self.session.query(sqla_models.Account).filter(sqla_models.Account.external_id == account_id)

            if for_update:
                base_query = base_query.with_for_update()

            django_account = base_query.one()
            return self._from_sqlalchemy_account_to_domain_account(django_account)

        except sqlalchemy.orm.exc.NoResultFound:
            return None

    def list(self, employee_id=None) -> List[domain.Account]:
        sqla_accounts = self.session.query(sqla_models.Account)

        if employee_id is not None:
            sqla_accounts = sqla_accounts.filter(employee_external_id=employee_id)

        return [self._from_sqlalchemy_account_to_domain_account(django_account) for django_account in sqla_accounts.all()]

    def add(self, account: domain.Account) -> domain.Account:
        sqla_account = sqla_models.Account(
            external_id=account.id,
            employee_external_id=account.employee_id,
            creation_date=account.activation_date,
            credits=account.credits
        )
        self.session.add(sqla_account)

        return self._from_sqlalchemy_account_to_domain_account(sqla_account)

    def update(self, account: domain.Account) -> domain.Account:
        try:
            self.session.begin_nested()

            sqla_account = self.session.query(sqla_models.Account).filter(
                sqla_models.Account.external_id == account.id
            ).one()

            sqla_account.employee_external_id = account.employee_id
            sqla_account.creation_date = account.activation_date
            sqla_account.credits = account.credits

            self.session.commit()

            return self._from_sqlalchemy_account_to_domain_account(sqla_account)
        except sqlalchemy.orm.exc.NoResultFound:
            raise AccountNotFoundException()

    @classmethod
    def _from_sqlalchemy_account_to_domain_account(cls, django_account: sqla_models.Account) -> domain.Account:
        return domain.Account(
            id=django_account.external_id,
            employee_id=django_account.employee_external_id,
            activation_date=django_account.creation_date,
            credits=django_account.credits
        )
