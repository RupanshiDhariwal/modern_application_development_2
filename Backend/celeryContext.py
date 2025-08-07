from celery import Task

from app import create_app
app, _, _ = create_app()

class ContextTask(Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return Task.__call__(self, *args, **kwargs)