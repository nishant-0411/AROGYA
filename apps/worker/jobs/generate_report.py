from apps.worker.queues.celery_app import celery_app

@celery_app.task
def generate_report_task(payload: dict):
    pass
