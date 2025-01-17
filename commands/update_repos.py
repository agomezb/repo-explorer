# coding=utf-8
import os
import sys

ruta = os.path.realpath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(ruta)

import typer

typer_app = typer.Typer()
from app.infraestructure.project_repository import ProjectRepository
from app.broker import sync_repos_task, sync_complementary_data_task


@typer_app.command()
def main():
    sync_repos_task.delay()

@typer_app.command()
def complementary():
    project_repository = ProjectRepository()
    projects = project_repository.get_all()
    for project in projects:
        sync_complementary_data_task.delay(project.id)


if __name__ == "__main__":
    typer_app()