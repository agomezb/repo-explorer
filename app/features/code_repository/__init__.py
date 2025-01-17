from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from app.domain.entities import CodeOwner, Project
from app.infraestructure.project_repository import ProjectRepository
from app.services.github_coderepository_service import GithubCodeRepositoryService


@dataclass
class FetchCodeRepositoriesRequest:
    pass

class FetchCodeRepositoriesHandler:

    def __init__(self):
        self.github_service = GithubCodeRepositoryService()
        self.project_repository = ProjectRepository()

    def handle(self, _: FetchCodeRepositoriesRequest):
        remote_repos = self.github_service.fetch_repos()
        for repo in remote_repos:
            project = Project(
                name=repo.name,
                url=repo.url,
                default_branch=repo.default_branch,
                external_id=repo.id,
                created_at=repo.created_at,
                last_commit_url=repo.last_commit_url,
                last_commit_date=repo.last_commit_date,
                description=repo.description
            )
            self.project_repository.save_basic_information(project)

class SyncComplentaryDataRequest(BaseModel):
    project_id:str

class SyncComplentaryDataHandler:

    def __init__(self):
        self.github_service = GithubCodeRepositoryService()
        self.project_repository = ProjectRepository()

    def handle(self, request: SyncComplentaryDataRequest):
        project = self.project_repository.get(request.project_id)
        remote_codeowners = self.github_service.fetch_codeowners(project.name)
        project.codeowners = [CodeOwner(**code_owner) for code_owner in remote_codeowners]
        self.project_repository.save(project)


