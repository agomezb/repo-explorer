from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class Entity(BaseModel):
    id: Optional[str] = None

class CodeOwner(BaseModel):
    path: str
    owners: List[str]

class Project(Entity):
    name: str
    url: str
    created_at: Optional[datetime] = None
    last_commit_url: Optional[str] = None
    last_commit_date: Optional[datetime] = None
    description: Optional[str] = None
    default_branch: Optional[str] = None
    external_id: Optional[str] = None
    codeowners : Optional[List[CodeOwner]] = None
    technology: Optional[str] = None

    def codeowners_join(self):
        join_names = ''
        if self.codeowners is None:
            return join_names
        for code_owner in self.codeowners:
            join_names += ','.join(code_owner.owners)
        return join_names

    def basic_dump(self):
        return self.model_dump(include={'name', 'url', 'default_branch',
                                        'external_id', 'created_at', 'last_commit_url',
                                        'technology','last_commit_date', 'description'})