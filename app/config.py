#!/usr/bin/python3

"""
Configurations for SQLAlchemy database
"""

import os


class Config:
    """
    Config class
    """

    SECRET_KEY = os.environ.get('SECRET_KEY', 'my_secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_secret_key_if_not_set')
