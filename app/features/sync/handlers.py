from typing import List

from pydantic import BaseModel

from app.config import settings
from app.domain.entities import CodeOwner, Project
from app.infraestructure.project_repository import ProjectRepository
from app.infraestructure.services.github_coderepository_service import GithubCodeRepositoryService, \
    LanguageRepositoryDto


class SyncBasicInformationRequest:
    pass

class SyncBasicInformationHandler:

    def __init__(self):
        self.github_service = GithubCodeRepositoryService()
        self.project_repository = ProjectRepository()

    def handle(self, _: SyncBasicInformationRequest):
        remote_repos = self.github_service.fetch_repos()
        for repo_dto in remote_repos:
            language_name = self.__max_language(repo_dto.languages)
            project = Project(**repo_dto.model_dump(),
                              external_id=repo_dto.id,
                              technology=language_name)
            self.project_repository.save_basic_information(project)

    def __max_language(self, languages: List[LanguageRepositoryDto]):
        if not languages:
            return None
        max_language = max(languages, key=lambda item: item.size)
        return max_language.name

class SyncComplentaryDataRequest(BaseModel):
    project_id:str

class SyncComplentaryDataHandler:

    def __init__(self):
        self.github_service = GithubCodeRepositoryService()
        self.project_repository = ProjectRepository()

    def handle(self, request: SyncComplentaryDataRequest):
        project = self.project_repository.get(request.project_id)
        remote_codeowners = self.github_service.fetch_codeowners(f"{settings.github_organization_name}/{project.name}")
        project.codeowners = [CodeOwner(**code_owner) for code_owner in remote_codeowners]
        self.project_repository.save(project)
