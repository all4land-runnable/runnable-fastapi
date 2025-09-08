# app/main.py
from dotenv import load_dotenv

from app.internal.exception.exception_handler import global_exception_handlers

# NOTE 1. 환경 변수 로딩
load_dotenv()

from fastapi import FastAPI
app = FastAPI(title="runnable-fastapi")

# NOTE 2. Base/engine은 DB 모듈에서 가져온다 (여기서 환경변수 읽힘)
from config.database.postgres_database import Base, engine

# NOTE 3. 모델 모듈 import: 매핑 등록을 위해 필수 (Users가 Base에 attach됨)
from app.routers.users import users_controller  # 변수 미사용이어도 OK. import 자체가 중요.
from app.routers.pace import paces_controller

# NOTE 4. 테이블 생성
Base.metadata.create_all(bind=engine)

# NOTE 5. 라우터 연결
app.include_router(users_controller.router, prefix='/api/v1', tags=['users'])
app.include_router(paces_controller.router, prefix="/api/v1", tags=["paces"])

# NOTE 6. 에러 핸들러 연결
global_exception_handlers(app)
