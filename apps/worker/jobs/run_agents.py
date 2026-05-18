from apps.worker.queues.celery_app import celery_app

@celery_app.task
def run_agents_task(payload: dict):
    pass
