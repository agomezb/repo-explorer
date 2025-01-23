import re
from datetime import datetime
from typing import Optional, List

from github import Auth, Github, UnknownObjectException, GithubException
from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport
from pydantic import BaseModel, model_serializer

from app.config import settings
from app.infraestructure.services.queries import query_get_repos

class LanguageRepositoryDto(BaseModel):
    name: str
    size: int

class CodeRepositoryDto(BaseModel):
    id: str
    name: str
    url: str
    created_at: Optional[datetime] = None
    default_branch: Optional[str] = None
    last_commit_url: Optional[str] = None
    last_commit_date: Optional[datetime] = None
    languages: List[LanguageRepositoryDto] = None
    description: Optional[str] = None

    def model_dump(self, **kwargs) -> dict:
        return super().model_dump(exclude={'id'}, **kwargs)


class GithubCodeRepositoryService:

    def __init__(self):
        self.organization_name = settings.github_organization_name
        self.token = settings.github_token
        self.github_client = Github(auth=Auth.Token(self.token))

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github.v4.idl",
        }
        transport = AIOHTTPTransport(url="https://api.github.com/graphql", headers=headers)
        self.graphql_client = Client(transport=transport, fetch_schema_from_transport=True)

    def fetch_repos(self) -> List[CodeRepositoryDto]:
        make_request = True
        repository_list = []
        query_params = {
            "organization": self.organization_name,
            "take": 100,
            "after": None
        }
        while make_request:
            code_repositories_response = self.graphql_client.execute(query_get_repos, variable_values=query_params)
            code_repositories_dict = code_repositories_response.get("organization").get("repositories").get("nodes")
            page_info_dict = code_repositories_response.get("organization").get("repositories").get("pageInfo")
            if page_info_dict and page_info_dict.get("hasNextPage") and page_info_dict.get("endCursor"):
                query_params["after"] = page_info_dict["endCursor"]
            else:
                make_request = False
            repository_list.extend(
                [self.__map_graphql_dto(item)
                 for item in code_repositories_dict]
            )
        return repository_list

    def __map_graphql_dto(self, code_repository_response) -> CodeRepositoryDto:
        branch_ref = code_repository_response.get('defaultBranchRef')
        branch_commit = branch_ref.get('target') if branch_ref else None
        return CodeRepositoryDto(
            id=code_repository_response["id"],
            name=code_repository_response["name"],
            url=code_repository_response["url"],
            created_at=code_repository_response["createdAt"],
            description=code_repository_response["description"],
            default_branch= branch_ref.get('name') if branch_ref else None,
            last_commit_date=branch_commit.get('committedDate') if branch_commit else None,
            languages=self.__map_languages(code_repository_response),
            last_commit_url=branch_commit.get('commitUrl') if branch_commit else None,)

    def __map_languages(self, code_repository_response):
        languages_dto = code_repository_response.get("languages",{})
        return [LanguageRepositoryDto(
                    name=language["node"].get("name"),
                    size=language["size"]) for language in languages_dto.get("edges", [])]

    async def fetch_repos_async(self) -> List[CodeRepositoryDto]:
        async with self.graphql_client as session:
            code_repositories_dict = await session.execute(query_get_repos)
            return [CodeRepositoryDto.model_validate(item) for item in code_repositories_dict]


    def fetch_codeowners(self, repository):
        repo = self.github_client.get_repo(repository)
        try:
            content_obj = repo.get_contents(".github/CODEOWNERS")
            if content_obj is None:
                return []
            return self.__map_codeowners(content_obj.decoded_content.decode("utf-8"))
        except (GithubException, UnknownObjectException):
            return []


    def __map_codeowners(self, codeowners_file_content: str):
        mylist = codeowners_file_content.split("\n")
        mylist = map(lambda x: x.strip(), mylist)
        return [
            {
                'path': re.split(r'\s+',line)[0],
                'owners': re.split(r'\s+', line)[1:]
            }
            for line in list(filter(lambda x: not x.startswith("#") and re.match(r"\S+\s+\S+", x), mylist))
        ]

