from flask import Flask
from zemfrog import loader
from celery import Celery

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

app = Flask(__name__)

with app.app_context():
    loader.load_config(app)
    loader.load_extensions(app)
    loader.load_models(app)
    loader.load_blueprints(app)
    loader.load_commands(app)
    loader.load_services(app)
    loader.load_schemas(app)

celery = make_celery(app)