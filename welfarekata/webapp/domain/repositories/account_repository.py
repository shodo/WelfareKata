from abc import ABCMeta, abstractmethod


class AccountRepository(metaclass=ABCMeta):
    @abstractmethod
    def get(self, account_id, for_update=False):
        pass

    @abstractmethod
    def list(self, employee_id=None):
        pass

    @abstractmethod
    def add(self, account):
        pass

    @abstractmethod
    def update(self, account):
        pass
