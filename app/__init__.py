from flask import Flask
from app.Model import db
from config import Config
from flask_migrate import Migrate

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()
    return app