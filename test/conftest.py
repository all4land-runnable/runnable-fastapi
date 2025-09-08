# tests/conftest.py
import os
from typing import Any, Generator

import pytest
from sqlalchemy import create_engine, event, URL
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool

from app.main import app
from config.database.postgres_database import Base
from config.database.postgres_database import get_database

POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_TEST_DATABASE = os.getenv('POSTGRES_TEST_DATABASE')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_PORT = int(os.getenv('POSTGRES_PORT'))

# 로컬 테스트 DB URL (개발 DB와 분리!)
TEST_SQLARCHEMY_DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    host=POSTGRES_HOST,
    database=POSTGRES_TEST_DATABASE,
    username=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    port=POSTGRES_PORT
)

# 테스트에서는 커넥션 풀 공유를 피하려고 NullPool 권장
engine = create_engine(TEST_SQLARCHEMY_DATABASE_URL, poolclass=NullPool, future=True)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, class_=Session)

@pytest.fixture(scope="session", autouse=True)
def _create_test_schema():
    # 마이그레이션을 쓰면, 여기서 Alembic을 돌리세요. (예: command.upgrade("head"))
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def db_session() -> Generator[Session | Any, Any, None]:
    """
    각 테스트를 트랜잭션으로 감싸고, 테스트 끝나면 롤백.
    서비스 내부 commit() 호출을 허용하기 위해 nested transaction 패턴 사용.
    """
    connection = engine.connect()
    transaction = connection.begin()            # 외부 트랜잭션
    session = TestingSessionLocal(bind=connection)

    # savepoint 시작
    session.begin_nested()

    # 내부에서 commit()이 호출되어도 savepoint 유지하도록 이벤트 훅
    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(sess, transaction):
        if transaction.nested and not transaction._parent.nested:
            sess.begin_nested()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()                  # 테스트 전체 롤백
        connection.close()

@pytest.fixture(autouse=True)
def override_get_db(db_session: Session):
    """
    FastAPI 의존성 오버라이드 → 앱 코드는 항상 이 세션을 사용.
    """
    def _get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_database] = _get_db
    yield
    app.dependency_overrides.clear()

@pytest.fixture()
def client(override_get_db):
    from fastapi.testclient import TestClient
    with TestClient(app) as client:
        yield client
