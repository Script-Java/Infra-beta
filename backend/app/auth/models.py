from fastapi_users.db import SQLAlchemyBaseUserTable, BaseUserManager, IntegerIDMixin
from sqlalchemy import Column, Boolean
from db import Base

class User(SQLAlchemyBaseUserTable[int], Base):
    is_active = Column(Boolean, default=True)

class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = "SECRET"
    verification_token_secret = "SECRET"