import threading

from celery import Celery

from app.config import settings

celery_app = Celery('repo_explorer',
                    broker=settings.rabbitmq_uri,
                    include=['app.features.sync.tasks'],
                    worker_concurrency=1)


class BrokerThread(threading.Thread):

    def __init__(self):
        super().__init__()

    def run(self):
        worker = celery_app.Worker()
        worker.start()

    def finish(self):
        print("broker thread finished")
        # TODO revisar logica de salida
