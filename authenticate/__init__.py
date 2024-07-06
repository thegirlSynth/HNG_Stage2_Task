#!/usr/bin/python3

"""
Initialises the app
"""

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .models import User, Organisation
