from abc import ABCMeta, abstractmethod


class PurchaseRepository(metaclass=ABCMeta):
    @abstractmethod
    def get(self, purchase_id):
        pass

    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def add(self, purchase):
        pass
