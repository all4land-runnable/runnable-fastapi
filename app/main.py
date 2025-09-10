# app/main.py
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware

from app.internal.exception.exception_handler import global_exception_handlers

# NOTE 1. 환경 변수 로딩
load_dotenv()

from fastapi import FastAPI
app = FastAPI(title="runnable-fastapi")

# 팔문 개방
origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# NOTE 2. Base/engine은 DB 모듈에서 가져온다 (여기서 환경변수 읽힘)
from config.database.postgres_database import Base, engine, ensure_postgis

# NOTE 3. 모델 모듈 import: 매핑 등록을 위해 필수 (Users가 Base에 attach됨)
from app.routers.pace_maker import pace_maker_controller
from app.routers.users import users_controller  # 변수 미사용이어도 OK. import 자체가 중요.
from app.routers.routes import routes_controller
from app.routers.categories import categories_controller
from app.routers.user_routes import user_routes_controller
from app.routers.user_strategies import user_strategies_controller
from app.routers.records import records_controller
from app.routers.ranks import ranks_controller
from app.routers.pace_records import pace_records_controller
from app.routers.sections import sections_controller
from app.routers.user_paces import user_paces_controller
from app.routers.route_geoms import route_geoms_controller
from app.routers.dataset import dataset_controller

# NOTE 4. 테이블 생성
ensure_postgis()
Base.metadata.create_all(bind=engine)

# NOTE 5. 라우터 연결
app.include_router(users_controller.router, prefix='/api/v1', tags=['users'])
app.include_router(routes_controller.router, prefix="/api/v1", tags=["routes"])
app.include_router(categories_controller.router, prefix="/api/v1", tags=["categories"])
app.include_router(pace_maker_controller.router, prefix="/api/v1", tags=["pace_maker"])
app.include_router(user_routes_controller.router, prefix="/api/v1", tags=["user_routes"])
app.include_router(user_strategies_controller.router, prefix="/api/v1", tags=["user_strategies"])
app.include_router(records_controller.router, prefix="/api/v1", tags=["records"])
app.include_router(ranks_controller.router, prefix="/api/v1", tags=["ranks"])
app.include_router(pace_records_controller.router, prefix="/api/v1", tags=["pace_records"])
app.include_router(sections_controller.router, prefix="/api/v1", tags=["sections"])
app.include_router(user_paces_controller.router, prefix="/api/v1", tags=["user_paces"])
app.include_router(route_geoms_controller.router, prefix="/api/v1", tags=["route_geoms"])
app.include_router(dataset_controller.router, prefix="/api/v1", tags=["dataset"])

# NOTE 6. 에러 핸들러 연결
global_exception_handlers(app)
