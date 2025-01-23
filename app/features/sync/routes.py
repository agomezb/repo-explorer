from fastapi import APIRouter

from app.infraestructure.project_repository import ProjectRepository
from .tasks import sync_repos_task, sync_complementary_data_task

sync_router = APIRouter(
    prefix="/sync",
    tags=["sync"],
    responses={404: {"description": "Not found"}},
)

@sync_router.get("/basic-information")
async def sync_basic_information():
    sync_repos_task.delay()


@sync_router.get("/complementary-information")
async def sync_complementary_information():
    project_repository = ProjectRepository()
    projects = project_repository.get_all()
    for project in projects:
        sync_complementary_data_task.delay(project.id)
