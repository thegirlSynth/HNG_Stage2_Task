#!/usr/bin/python3

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

from routes import my_app
app.register_blueprint(my_app)


with app.app_context():
    from models import User, Organisation
    db.create_all()


migrate = Migrate(app, db)
jwt = JWTManager(app)
