# from flask import Flask
# from applications.database import db
# import os
# from flask_jwt_extended import JWTManager
# from applications import workers


# app = Flask(__name__)
# app.config["JWT_SECRET_KEY"]="anything"

# jwt_mgr=JWTManager(app)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+os.path.join(os.getcwd(),"database_files/influencer_app.db")
# app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/1"
# app.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/2"

# app.config["CACHE_TYPE"] = "RedisCache"
# app.config["CACHE_REDIS_URL"] = "redis://localhost:6379/3"
# app.config["CELERY_DEFAULT_TIMEOUT"] = 200
# app.config["REDIS_URL"] = "redis://localhost:6379"
# app.config["broker_url"] = "redis://localhost:6379/0"
# app.config["result_backend"] = "redis://localhost:6379/0"
# app.config["broker_connection_retry_on_startup"] = True

# # app.app_context().push()

# db.init_app(app)
# # app.app_context().push()

# celery = workers.celery
# celery.conf.update(broker_url=app.config["CELERY_BROKER_URL"], result_backend = app.config["CELERY_RESULT_BACKEND"] ,imports=("tasks",) )
# celery.Task = workers.ContextTask
# app.app_context().push()

# from applications.admin_routes import *
# from applications.user_routes import *
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port = 8080,debug=True)


from flask import Flask
from applications.database import db
import os
from flask_jwt_extended import JWTManager
from applications import workers
from flask_cors import CORS
# from applications.cache import cache


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "anything"

jwt_mgr = JWTManager(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(os.getcwd(), "database_files/influencer_app.db")
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/1"
app.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/2"

app.config["CACHE_TYPE"] = "RedisCache"
app.config["CACHE_REDIS_URL"] = "redis://localhost:6379/3"
app.config["CELERY_DEFAULT_TIMEOUT"] = 200
app.config["REDIS_URL"] = "redis://localhost:6379"
app.config["broker_url"] = "redis://localhost:6379/0"
app.config["result_backend"] = "redis://localhost:6379/0"
app.config["broker_connection_retry_on_startup"] = True

db.init_app(app)

celery = workers.celery
celery.conf.update(
    broker_url=app.config["CELERY_BROKER_URL"],
    result_backend=app.config["CELERY_RESULT_BACKEND"],
    imports=("applications.tasks",)  # Make sure this is correctly pointing to tasks module
)
celery.Task = workers.ContextTask

# cache.init_app(app)
CORS(app)
app.app_context().push()



from applications.admin_routes import *
from applications.user_routes import *

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

