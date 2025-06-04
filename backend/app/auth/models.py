from fastapi_users.db import SQLAlchemyBaseUserTable
from fastapi_users.manager import BaseUserManager, IntegerIDMixin
from sqlalchemy import Column, Boolean
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTable[int], Base):
    is_active = Column(Boolean, default=True)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = "SECRET"
    verification_token_secret = "SECRET"
