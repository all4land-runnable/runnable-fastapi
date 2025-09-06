# app/main.py
from dotenv import load_dotenv
load_dotenv()  # 1) .env를 가장 먼저 로드해야 engine이 환경변수를 제대로 읽는다.

from fastapi import FastAPI
app = FastAPI(title="runnable-fastapi")

# 2) Base/engine은 DB 모듈에서 가져온다 (여기서 환경변수 읽힘)
from config.database.postgres_database import Base, engine

# 3) 모델 모듈 import: 매핑 등록을 위해 필수 (Users가 Base에 attach됨)
from app.routers.users import users_controller  # 변수 미사용이어도 OK. import 자체가 중요.
from app.routers.pace import paces_controller

# 4) 테이블 생성 (개발용)
Base.metadata.create_all(bind=engine)

# 5) 라우터 연결
app.include_router(users_controller.router, prefix='/api', tags=['users'])
app.include_router(paces_controller.router, prefix="/api", tags=["paces"])
