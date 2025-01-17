from typing import Any, Mapping

from bson import ObjectId
from pymongo import MongoClient

from app.domain.entities import Project


class ProjectRepository:

    def __init__(self):
        self._client = MongoClient("", tlsInsecure=True)
        database = self._client['RepoExplorer']
        self._collection = database["project"]

    def save(self, project: Project):
        if project.id is None:
            return self.create(project)
        return self.update(project)

    def create(self, project: Project):
        result = project.model_dump()
        current_id = result.get("id")
        if current_id:
            result['_id'] = result['id']
        del result['id']
        return self._collection.insert_one(result).inserted_id

    def update(self, project: Project):
        data = project.model_dump()
        project_id = data['id']
        del data['id']
        self._collection.update_one({'_id': ObjectId(project_id)}, {"$set": data})
        return project_id

    def save_basic_information(self, project: Project):
        data = {
            'name': project.name,
            'url': project.url,
            'default_branch': project.default_branch,
            'external_id': project.external_id,
            'created_at': project.created_at,
            'last_commit_url': project.last_commit_url,
            'last_commit_date': project.last_commit_date,
            'description': project.description
        }
        self._collection.update_one({'external_id': data['external_id']}, {"$set": data}, upsert=True)

    def get(self, project_id: str):
        dict_obj = self._collection.find_one({"_id": ObjectId(project_id)})
        if dict_obj:
            return Project(**self.__process(dict_obj))
        return None

    def get_all(self):
        dict_list = self._collection.find()
        if dict_list:
            return [Project(**self.__process(dict_obj)) for dict_obj in dict_list]
        return None

    def __process(self, dict_obj: Mapping[str, Any]):
        dict_obj['id'] = str(dict_obj['_id'])
        return dict_obj