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
