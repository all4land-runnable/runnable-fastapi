# tests/test_categories_crud.py
from uuid import uuid4

USERS_API = "/api/v1/users"
CATS_API = "/api/v1/categories"

def _mk_user_payload():
    return {
        "email": f"test+{uuid4().hex[:6]}@all4land.com",
        "password": "abcd1234",
        "username": f"올포랜드-{uuid4().hex[:6]}",
        "age": 28,
        "runner_since": 2022,
        "pace_average": 390,
    }

def _mk_category_payload(user_id: int, name: str | None = None):
    return {
        "user_id": user_id,
        "name": name or f"카테고리-{uuid4().hex[:6]}",
    }

def _create_user(client) -> int:
    # 테스트용 유저 생성 → user_id 반환
    res = client.post(USERS_API, json=_mk_user_payload())
    assert res.status_code == 201
    return res.json()["data"]["user_id"]

def test_create_read_update_delete_category(client):
    user_id = _create_user(client)

    # NOTE 1. Create
    payload = _mk_category_payload(user_id)
    res = client.post(CATS_API, json=payload, headers={"accept": "application/json"})
    assert res.status_code == 201
    body = res.json()
    assert body["code"] == 201
    assert body["message"] == "카테고리 생성 성공"

    data = body["data"]
    category_id = data["category_id"]
    assert data["user_id"] == user_id
    assert data["name"] == payload["name"]

    # NOTE 2. Read by id
    res = client.get(f"{CATS_API}/{category_id}")
    assert res.status_code == 200
    got = res.json()["data"]
    assert got["category_id"] == category_id
    assert got["name"] == payload["name"]

    # NOTE 3. Read list
    res = client.get(CATS_API)
    assert res.status_code == 200
    lst = res.json()["data"]
    assert isinstance(lst, list)
    assert any(c["category_id"] == category_id for c in lst)

    # NOTE 4. Update
    patched_name = f"{payload['name']}-patched"
    patch_body = {
        "category_id": category_id,
        "name": patched_name,
    }
    res = client.patch(CATS_API, json=patch_body)
    assert res.status_code == 200
    got = res.json()["data"]
    assert got["category_id"] == category_id
    assert got["name"] == patched_name

    # NOTE 5. 업데이트 결과 재검증
    res = client.get(f"{CATS_API}/{category_id}")
    assert res.status_code == 200
    got = res.json()["data"]
    assert got["name"] == patched_name

    # NOTE 6. Delete
    res = client.delete(f"{CATS_API}/{category_id}")
    assert res.status_code == 200
    body = res.json()
    assert body["code"] == 200
    assert body["message"] == "카테고리 삭제 성공"

    # NOTE 7. 삭제 후 조회 시 Not Found 매핑 확인
    res = client.get(f"{CATS_API}/{category_id}")
    assert res.status_code == 400
    body = res.json()
    assert body["code"] == 404
    assert body["message"] == "카테고리를 찾을 수 없습니다."

def test_create_duplicate_category_name_should_fail(client):
    """
    같은 user_id 에서 같은 name으로 2회 생성 시 실패해야 함.
    """
    user_id = _create_user(client)

    p1 = _mk_category_payload(user_id, name="중복체크")
    res = client.post(CATS_API, json=p1)
    assert res.status_code == 201

    p2 = _mk_category_payload(user_id, name="중복체크")  # 같은 유저 + 같은 이름
    res = client.post(CATS_API, json=p2)

    # 전역 핸들러에 의해 400으로 매핑
    assert res.status_code == 400
    body = res.json()
    assert body["code"] == 404
    assert body["message"] == "중복된 카테고리명 입니다."
