#!/usr/bin/python3

"""
User Model
"""

from . import db


class User(db.Model):
    """
    User Model
    """

    __tablename__ = "users"

    userId = db.Column(db.String, unique=True, primary_key=True, index=True)
    firstName = db.Column(db.String, nullable=False)
    lastName = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    phone = db.Column(db.String)


class Organisation(db.Model):
    """
    Organisation Model
    """

    __tablename__ = "organisation"

    orgId = db.Column(db.String, unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    user_id = db.Column(db.String, db.ForeignKey('user.userId'))
    user = db.relationship('User', backref=db.backref('organisations', lazy=True))
