from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from app.config import config
from app.routes.route import RouteMainApp

db = SQLAlchemy()


def create_app() -> Flask:
    app_context = os.getenv("FLASK_ENV")
    app = Flask(__name__)

    f = config.factory(app_context if app_context else "development")
    app.config.from_object(f)

    route = RouteMainApp()
    route.init_app(app)

    db.init_app(app)
    migrate = Migrate(app, db)
    migrate.init_app(app, db)

    return app
