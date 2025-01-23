from app.config.broker import celery_app

from app.config.cqrs import mediator
from app.features.sync.handlers import SyncComplentaryDataRequest, SyncBasicInformationRequest


@celery_app.task
def sync_repos_task():
    request = SyncBasicInformationRequest()
    mediator.send(request)


@celery_app.task
def sync_complementary_data_task(project_id:str):
    request = SyncComplentaryDataRequest(project_id=project_id)
    mediator.send(request)