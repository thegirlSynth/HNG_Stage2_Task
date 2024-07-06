#!/usr/bin/python3

"""
User Model
"""

from sqlalchemy import Column, Integer, String
from sqlachemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    User Model
    """

    __tablename__ = "users"

    userId = Column(String, unique=True, primary_key=True, index=True)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    phone = Column(String)


class Organisation(Base):
    """
    Organisation Model
    """

    __tablename__ = "organisation"

    orgId = Column(String, unique=True, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
