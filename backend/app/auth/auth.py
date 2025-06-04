# main.py
from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTStrategy
from .models import User, UserManager
from ..duckdb_services import async_session_maker

SECRET = "SECRET"

async def get_user_manager():
    yield UserManager(User, async_session_maker)

auth_backend = JWTStrategy(secret=SECRET, lifetime_seconds=3600)

fastapi_users = FastAPIUsers(
    get_user_manager,
    [auth_backend],
    User,
)

app = FastAPI()

app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt")
app.include_router(fastapi_users.get_register_router(), prefix="/auth")
app.include_router(fastapi_users.get_users_router(), prefix="/users")
