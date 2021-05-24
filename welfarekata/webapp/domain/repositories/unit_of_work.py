import abc


class UnitOfWork(abc.ABC):
    def __enter__(self) -> 'UnitOfWork':
        return self

    def __exit__(self, *args):
        pass
