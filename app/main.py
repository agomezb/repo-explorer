from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from starlette.templating import Jinja2Templates

from app.broker import BrokerThread
from app.infraestructure.project_repository import ProjectRepository

broker_thread = BrokerThread()

@asynccontextmanager
async def lifespan(_: FastAPI):
    broker_thread.start()
    yield
    broker_thread.finish()

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_items(request: Request):
    project_repository = ProjectRepository()
    projects = project_repository.get_all()
    return templates.TemplateResponse(
        request=request, name="projects.html", context={"projects": projects})

