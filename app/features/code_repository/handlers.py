from app.infraestructure.project_repository import ProjectRepository


class GetCodeRepositoryRequest:
    pass

class GetCodeRepositoryRequestHandler:

    def __init__(self):
        self.project_repository = ProjectRepository()

    def handle(self, _: GetCodeRepositoryRequest):
        project_repository = ProjectRepository()
        return project_repository.get_all()


