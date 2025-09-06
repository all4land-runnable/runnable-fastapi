from datetime import datetime
from typing import Optional

from app.routers.users.users import Users
from config.database.postgres_database import PostgresDatabase

database = PostgresDatabase()

def create_users() -> str:
    database.execute_update(
        sql="CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, email VARCHAR(255) NOT NULL UNIQUE, password VARCHAR(255) NOT NULL, username VARCHAR(255) NOT NULL, created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)"
    )
    return "users 테이블이 생성되었습니다."

def drop_users() -> str:
    database.execute_update(
        sql="DROP TABLE IF EXISTS users"
    )
    return "users 테이블이 삭제되었습니다."

def has_tone()->bool:
    return 1 == database.execute_query(
        sql="SELECT 1 FROM Information_schema.tables WHERE table_name = 'users' AND table_schema = 'public'"
    )

def insert_into(user: Users) -> Users:
    database.execute_update(
        sql="INSERT INTO users (email, password, username, created_at, updated_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
        values=(user.email, user.password, user.username, user.created_at, datetime.now()),
    )
    return user

def update_into(user: Users) -> Users:
    database.execute_update(
        sql="UPDATE users SET email=%s, password=%s, username=%s, updated_at=CURRENT_TIMESTAMP WHERE id = %s",
        values=(user.email, user.password, user.username, user.id),
    )
    return user

def upsert_into(user: Users) -> Users:
    user = database.execute_query(
        sql="""
        INSERT INTO public.users (email, password, username)
        VALUES (%s, %s, %s)
        ON CONFLICT (email) DO UPDATE
          SET password   = EXCLUDED.password,
              username   = EXCLUDED.username,
              updated_at = CURRENT_TIMESTAMP
        RETURNING id, email, password, username, created_at, updated_at
        """,
        values=(user.email, user.password, user.username),
    )
    return user

def save(user: Users) -> Users:
    return update_into(user)

def delete_users(user: Users) -> Users:
    database.execute_update(
        sql="DELETE FROM users WHERE id = %s",
        values=(user.id,),
    )
    return user

def has_user(id: int) -> bool:
    user = database.execute_query(
        sql="SELECT * FROM users WHERE id = %s",
        values=(id,),
    )
    return bool(user)

def find_by_id(id: int) -> Optional[Users]:
    user = database.execute_query(
        sql="SELECT * FROM users WHERE id = %s",
        values=(id,)
    )
    return Users(**user[0]) if user else None

def find_by_email(email: str) -> Optional[Users]:
    user = database.execute_query(
        sql="SELECT * FROM users WHERE email = %s",
        values=(email,)
    )
    return Users(**user[0]) if user else None

def find_by_username(username: str) -> Optional[Users]:
    user = database.execute_query(
        sql="SELECT * FROM users WHERE username = %s",
        values=(username,)
    )
    return Users(**user[0]) if user else None

def find_all() -> Optional[list[Users]]:
    users = database.execute_query(
        sql="SELECT * FROM public.users"
    )
    return [Users(**user) for user in users]
