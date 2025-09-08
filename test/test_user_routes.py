# tests/test_user_routes_crud.py
from uuid import uuid4

USERS_API = "/api/v1/users"
CATS_API = "/api/v1/categories"
ROUTES_API = "/api/v1/routes"
UR_API = "/api/v1/user-routes"

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

def _mk_route_payload():
    return {
        "title": f"루트-{uuid4().hex[:6]}",
        "description": "테스트 루트",
        "distance": 5000,
        "high_height": 123.4,
        "low_height": 12.3,
    }

def _mk_user_route_payload(user_id: int, category_id: int, route_id: int):
    return {
        "user_id": user_id,
        "category_id": category_id,
        "route_id": route_id,
    }

def _create_user(client) -> int:
    res = client.post(USERS_API, json=_mk_user_payload())
    assert res.status_code == 201
    return res.json()["data"]["user_id"]

def _create_category(client, user_id: int) -> int:
    res = client.post(CATS_API, json=_mk_category_payload(user_id))
    assert res.status_code == 201
    return res.json()["data"]["category_id"]

def _create_route(client) -> int:
    res = client.post(ROUTES_API, json=_mk_route_payload())
    assert res.status_code == 201
    return res.json()["data"]["route_id"]

def test_create_read_update_delete_user_route(client):
    # 준비: user, category, route 생성
    user_id = _create_user(client)
    category_id = _create_category(client, user_id)
    route_id = _create_route(client)

    # NOTE 1. Create
    payload = _mk_user_route_payload(user_id, category_id, route_id)
    res = client.post(UR_API, json=payload, headers={"accept": "application/json"})
    assert res.status_code == 201

    body = res.json()
    assert body["code"] == 201
    assert body["message"] == "유저-루트 매핑 생성 성공"

    data = body["data"]
    user_route_id = data["user_route_id"]
    assert data["user_id"] == user_id
    assert data["category_id"] == category_id
    assert data["route_id"] == route_id

    # NOTE 2. Read by id
    res = client.get(f"{UR_API}/{user_route_id}")
    assert res.status_code == 200
    got = res.json()["data"]
    assert got["user_route_id"] == user_route_id

    # NOTE 3. Read list
    res = client.get(UR_API)
    assert res.status_code == 200
    lst = res.json()["data"]
    assert isinstance(lst, list)
    assert any(ur["user_route_id"] == user_route_id for ur in lst)

    # NOTE 4. Update (category 변경)
    # 새로운 카테고리 생성 후 매핑 변경
    new_category_id = _create_category(client, user_id)
    patch_body = {
        "user_route_id": user_route_id,
        "category_id": new_category_id,
    }
    res = client.patch(UR_API, json=patch_body)
    assert res.status_code == 200
    got = res.json()["data"]
    assert got["user_route_id"] == user_route_id
    assert got["category_id"] == new_category_id

    # NOTE 5. 업데이트 결과 재검증
    res = client.get(f"{UR_API}/{user_route_id}")
    assert res.status_code == 200
    assert res.json()["data"]["category_id"] == new_category_id

    # NOTE 6. Delete
    res = client.delete(f"{UR_API}/{user_route_id}")
    assert res.status_code == 200
    body = res.json()
    assert body["code"] == 200
    assert body["message"] == "유저-루트 매핑 삭제 성공"

    # NOTE 7. 삭제 후 조회는 Not Found
    res = client.get(f"{UR_API}/{user_route_id}")
    assert res.status_code == 400
    body = res.json()
    assert body["code"] == 404
    assert body["message"] == "사용자-루트 매핑을 찾을 수 없습니다."

def test_create_duplicate_user_route_should_fail(client):
    user_id = _create_user(client)
    category_id = _create_category(client, user_id)
    route_id = _create_route(client)

    p1 = _mk_user_route_payload(user_id, category_id, route_id)
    res = client.post(UR_API, json=p1)
    assert res.status_code == 201

    # 동일 triplet 재시도 → UniqueViolation → 전역 핸들러 400
    p2 = _mk_user_route_payload(user_id, category_id, route_id)
    res = client.post(UR_API, json=p2)
    assert res.status_code == 400

    body = res.json()
    assert body["code"] == 404
    assert body["message"] == "중복된 사용자-카테고리-루트 매핑입니다."
