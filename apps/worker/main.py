import sys
from apps.worker.queues.celery_app import celery_app

def main():
    argv = ["worker", "--loglevel=INFO"]
    if len(sys.argv) > 1:
        argv.extend(sys.argv[1:])
    celery_app.worker_main(argv)

if __name__ == "__main__":
    main()
