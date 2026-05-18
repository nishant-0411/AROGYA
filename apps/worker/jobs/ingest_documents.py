from apps.worker.queues.celery_app import celery_app

@celery_app.task
def ingest_documents_task(payload: dict):
    pass
