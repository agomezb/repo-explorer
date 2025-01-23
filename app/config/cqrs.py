from pymediator import Mediator as _Mediator, SingletonRegistry

from app.features.code_repository.handlers import GetCodeRepositoryRequest, GetCodeRepositoryRequestHandler
from app.features.sync.handlers import (SyncBasicInformationRequest, SyncBasicInformationHandler,
                                        SyncComplentaryDataRequest, SyncComplentaryDataHandler)

registry: SingletonRegistry = SingletonRegistry()
registry.register(SyncBasicInformationRequest, SyncBasicInformationHandler)
registry.register(SyncComplentaryDataRequest, SyncComplentaryDataHandler)
registry.register(GetCodeRepositoryRequest, GetCodeRepositoryRequestHandler)

class Mediator(_Mediator):
    def __init__(self) -> None:
        super().__init__(registry=SingletonRegistry())

mediator: Mediator = Mediator()
