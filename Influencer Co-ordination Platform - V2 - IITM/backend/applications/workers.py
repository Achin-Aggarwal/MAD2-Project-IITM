# from celery import Celery, Task
# from flask import current_app as app

# celery = Celery("Application Jobs")

# class ContextTask(Task):
#     def __call__(self, *args, **kwargs):
#         with app.app_context():
#             return super().__call__(*args, **kwargs)  # Use the base call method

# celery.Task = ContextTask  # Set the task base class in celery

# # Ensure no redundant imports or circular references exist
from celery import Celery, Task
from flask import current_app as app

celery = Celery("Application Jobs")

class ContextTask(Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return super().__call__(*args, **kwargs)

celery.Task = ContextTask  # Set the task base class in celery
