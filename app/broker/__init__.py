import threading

from celery import Celery

from app.config import mediator
from app.features.code_repository import FetchCodeRepositoriesRequest, SyncComplentaryDataRequest

app = Celery('repo_explorer',
             broker='',
             worker_concurrency=1)



@app.task
def sync_repos_task():
    request = FetchCodeRepositoriesRequest()
    print(mediator.send(request))


@app.task
def sync_complementary_data_task(project_id:str):
    request = SyncComplentaryDataRequest(project_id=project_id)
    print(mediator.send(request))


class BrokerThread(threading.Thread):

    def __init__(self):
        super().__init__()

    def run(self):
        worker = app.Worker()
        worker.start()

    def finish(self):
        print("broker thread finished")
        # TODO revisar logica de salida
