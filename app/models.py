#!/usr/bin/python3

"""
User and Organisation Models with Many-to-Many Relationship
"""

from app import db


# Association table for many-to-many relationship
user_organisation = db.Table('user_organisation',
                             db.Column('user_id', db.String, db.ForeignKey('users.userId'), primary_key=True),
                             db.Column('org_id', db.String, db.ForeignKey('organisations.orgId'), primary_key=True)
                             )


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

    # Define the many-to-many relationship with Organisation
    organisations = db.relationship('Organisation', secondary=user_organisation, backref=db.backref('users', lazy=True))


class Organisation(db.Model):
    """
    Organisation Model
    """

    __tablename__ = "organisations"

    orgId = db.Column(db.String, unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
