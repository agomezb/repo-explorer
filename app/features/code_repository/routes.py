from fastapi import APIRouter

from app.config.cqrs import mediator
from app.features.code_repository.handlers import GetCodeRepositoryRequest

project_router = APIRouter(
    prefix="/project",
    tags=["project"],
    responses={404: {"description": "Not found"}},
)

@project_router.get("/")
async def read_items():
    request = GetCodeRepositoryRequest()
    return mediator.send(request)
