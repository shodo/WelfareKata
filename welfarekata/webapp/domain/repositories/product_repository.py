from abc import ABCMeta, abstractmethod


class ProductRepository(metaclass=ABCMeta):
    @abstractmethod
    def get(self, product_id):
        pass

    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def add(self, product):
        pass

    @abstractmethod
    def update(self, product):
        pass
