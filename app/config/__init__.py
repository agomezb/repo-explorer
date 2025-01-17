
from pymediator import Mediator as _Mediator, SingletonRegistry

from app.features.code_repository import FetchCodeRepositoriesRequest, FetchCodeRepositoriesHandler, \
    SyncComplentaryDataRequest, SyncComplentaryDataHandler

registry: SingletonRegistry = SingletonRegistry()
registry.register(FetchCodeRepositoriesRequest, FetchCodeRepositoriesHandler)
registry.register(SyncComplentaryDataRequest, SyncComplentaryDataHandler)


class Mediator(_Mediator):
    def __init__(self) -> None:
        super().__init__(registry=SingletonRegistry())

mediator: Mediator = Mediator()