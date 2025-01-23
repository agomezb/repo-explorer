from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from starlette.templating import Jinja2Templates

from app.config import settings
from app.config.broker import BrokerThread
from app.features.code_repository.routes import project_router
from app.features.sync.routes import sync_router
from app.infraestructure.project_repository import ProjectRepository

broker_thread = BrokerThread()

@asynccontextmanager
async def lifespan(_: FastAPI):
    broker_thread.start()
    yield
    broker_thread.finish()

app = FastAPI(lifespan=None)
templates = Jinja2Templates(directory="templates")
app.include_router(project_router)
app.include_router(sync_router)

@app.get("/")
async def read_items(request: Request):
    project_repository = ProjectRepository()
    projects = project_repository.get_all()
    return templates.TemplateResponse(
        request=request, name="projects.html", context={"projects": projects})


@app.get("/settings")
def get_settings():
    return settings