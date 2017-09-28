import os
from celery import Celery
from flask import Flask


def make_flask_app(name, environment):
    env_config = "LocalDevelopment"
    if environment == "staging":
        env_config = "StagingConfig"
    elif environment == "production":
        env_config = "ProductionConfig"

    app = Flask(name)
    app.config.from_object('config.{}'.format(env_config))

    return app


def make_celery(app):
    celery = Celery('tasks',
                    broker=os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
                    backend=os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'))
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery
