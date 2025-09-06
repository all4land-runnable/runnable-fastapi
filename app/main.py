from dotenv import load_dotenv

from app.routers.users.ㅅ드ㅔ import models
from config.database.postgres_database import engine

load_dotenv()

from fastapi import FastAPI

from app.routers.users.users_controller import router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="runnable-fastapi")

app.include_router(router)