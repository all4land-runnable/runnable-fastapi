import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Generator

POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_PORT = int(os.getenv('POSTGRES_PORT'))

# database 생성 URL
SQLARCHEMY_DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    host=POSTGRES_HOST,
    database=POSTGRES_DATABASE,
    username=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    port=POSTGRES_PORT
)

# Engine 구축
# Engine: SqlAlchemy에서 데이터베이스와 연결을 생성하는 객체
engine = create_engine(
    SQLARCHEMY_DATABASE_URL,
    pool_pre_ping=True, # 죽은 커넥션 자동 복구
)

# Session 구현
# Session: ORM이 실제로 DB와 통신할 때 사용하는 작업 단위 (add, commit, query 등 처리)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
Base = declarative_base()

def get_database() -> Generator[Session, None, None]:
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


def ensure_postgis():
    # DB에 접속해 PostGIS 확장을 켭니다. (권한 없으면 그냥 무시)
    try:
        with engine.begin() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
    except Exception:
        # RDS 등에서 권한이 없을 수 있음 → 애플리케이션은 계속 구동
        pass