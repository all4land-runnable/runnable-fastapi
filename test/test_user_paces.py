# tests/test_user_paces_crud.py
from uuid import uuid4

USERS_API = "/api/v1/users"
ROUTES_API = "/api/v1/routes"
CATEGORIES_API = "/api/v1/categories"
USER_ROUTES_API = "/api/v1/user-routes"
USER_STRATEGIES_API = "/api/v1/user-strategies"
SECTIONS_API = "/api/v1/sections"
USER_PACES_API = "/api/v1/user-paces"

def _mk_user_payload():
    return {
        "email": f"test+{uuid4().hex[:6]}@all4land.com",
        "password": "abcd1234",
        "username": f"올포랜드-{uuid4().hex[:6]}",
        "age": 28,
        "runner_since": 2022,
        "pace_average": 390,
    }

def _mk_route_payload():
    return {
        "title": f"테스트루트-{uuid4().hex[:6]}",
        "description": "테스트용 경로",
        "distance": 5000,
        "high_height": 123.4,
        "low_height": 12.3,
    }

def _mk_category_payload(user_id: int):
    return {
        "user_id": user_id,
        "name": f"카테고리-{uuid4().hex[:4]}",
    }

def _mk_user_route_payload(user_id: int, category_id: int, route_id: int):
    return {
        "user_id": user_id,
        "category_id": category_id,
        "route_id": route_id,
    }

def _mk_user_strategy_payload(user_route_id: int):
    return {
        "user_route_id": user_route_id,
        "luggage_weight": 3,
        "pace_average": 380,
    }

def _mk_section_payload(route_id: int):
    return {
        "route_id": route_id,
        "start_latitude": 37.501,
        "start_longitude": 127.001,
        "start_height": 12.0,
        "end_latitude": 37.511,
        "end_longitude": 127.011,
        "end_height": 18.5,
        "slope": 3,
    }

def _mk_user_pace_payload(user_strategy_id: int, section_id: int):
    return {
        "user_strategy_id": user_strategy_id,
        "section_id": section_id,
        "pace": 370,
        "strategy": "steady",
        "foundation_latitude": 37.505,
        "foundation_longitude": 127.005,
    }

def test_user_paces_crud(client):
    # 1) user
    u_res = client.post(USERS_API, json=_mk_user_payload())
    assert u_res.status_code == 201
    user_id = u_res.json()["data"]["user_id"]

    # 2) route
    r_res = client.post(ROUTES_API, json=_mk_route_payload())
    assert r_res.status_code == 201
    route_id = r_res.json()["data"]["route_id"]

    # 3) category
    c_res = client.post(CATEGORIES_API, json=_mk_category_payload(user_id))
    assert c_res.status_code == 201
    category_id = c_res.json()["data"]["category_id"]

    # 4) user_route
    ur_res = client.post(USER_ROUTES_API, json=_mk_user_route_payload(user_id, category_id, route_id))
    assert ur_res.status_code == 201
    user_route_id = ur_res.json()["data"]["user_route_id"]

    # 5) user_strategy
    us_res = client.post(USER_STRATEGIES_API, json=_mk_user_strategy_payload(user_route_id))
    assert us_res.status_code == 201
    user_strategy_id = us_res.json()["data"]["user_strategy_id"]

    # 6) section
    s_res = client.post(SECTIONS_API, json=_mk_section_payload(route_id))
    assert s_res.status_code == 201
    section_id = s_res.json()["data"]["section_id"]

    # 7) user_pace 생성
    up_payload = _mk_user_pace_payload(user_strategy_id, section_id)
    res = client.post(USER_PACES_API, json=up_payload)
    assert res.status_code == 201
    body = res.json()
    assert body["code"] == 201
    assert body["message"] == "유저 페이스 생성 성공"

    data = body["data"]
    user_pace_id = data["user_pace_id"]
    assert data["user_strategy_id"] == user_strategy_id
    assert data["section_id"] == section_id

    # 8) 개별 조회
    res = client.get(f"{USER_PACES_API}/{user_pace_id}")
    assert res.status_code == 200
    got = res.json()["data"]
    assert got["user_pace_id"] == user_pace_id
    assert got["pace"] == up_payload["pace"]

    # 9) strategy로 조회
    res = client.get(f"{USER_PACES_API}/strategy/{user_strategy_id}")
    assert res.status_code == 200
    lst = res.json()["data"]
    assert any(x["user_pace_id"] == user_pace_id for x in lst)

    # 10) section으로 조회
    res = client.get(f"{USER_PACES_API}/section/{section_id}")
    assert res.status_code == 200
    lst = res.json()["data"]
    assert any(x["user_pace_id"] == user_pace_id for x in lst)

    # 11) 전체 조회
    res = client.get(USER_PACES_API)
    assert res.status_code == 200
    lst = res.json()["data"]
    assert isinstance(lst, list)
    assert any(x["user_pace_id"] == user_pace_id for x in lst)

    # 12) 부분 수정
    patched = {
        "user_pace_id": user_pace_id,
        "pace": 360,
        "strategy": "progressive",
        "foundation_latitude": 37.506,
    }
    res = client.patch(USER_PACES_API, json=patched)
    assert res.status_code == 200
    got = res.json()["data"]
    assert got["user_pace_id"] == user_pace_id
    assert got["pace"] == 360
    assert got["strategy"] == "progressive"
    assert got["foundation_latitude"] == 37.506

    # 13) 삭제
    res = client.delete(f"{USER_PACES_API}/{user_pace_id}")
    assert res.status_code == 200
    assert res.json()["message"] == "유저 페이스 삭제 성공"

    # 14) 삭제 후 조회 → 400 + USER_PACE_NOT_FOUND
    res = client.get(f"{USER_PACES_API}/{user_pace_id}")
    assert res.status_code == 400
    body = res.json()
    assert body["code"] == 404
    assert body["message"] == "사용자 페이스를 찾을 수 없습니다."
