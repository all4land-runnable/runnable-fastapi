# tests/test_routes_crud.py
from uuid import uuid4

API_BASE = "/api/v1/routes"


def _mk_route_payload():
    """
    라우트 생성 페이로드. title/description에 유니크한 값 부여(관찰 편의를 위해).
    """
    salt = uuid4().hex[:6]
    return {
        "title": f"경로-{salt}",
        "description": f"테스트 경로 설명-{salt}",
        "distance": 5000,      # m 단위 예시
        "high_height": 123.4,  # 최고 고도
        "low_height": 12.3,    # 최저 고도
    }


def test_create_read_update_delete_route(client):
    # NOTE 1. Create
    payload = _mk_route_payload()
    res = client.post(API_BASE, json=payload, headers={"accept": "application/json"})
    assert res.status_code == 201

    body = res.json()
    assert body["code"] == 201
    assert body["message"] == "경로 생성 성공"

    data = body["data"]
    assert "route_id" in data
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["distance"] == payload["distance"]
    assert float(data["high_height"]) == payload["high_height"]
    assert float(data["low_height"]) == payload["low_height"]

    # NOTE 2. Read by id
    route_id = data["route_id"]
    res = client.get(f"{API_BASE}/{route_id}")
    assert res.status_code == 200
    got = res.json()["data"]
    assert got["route_id"] == route_id
    assert got["title"] == payload["title"]

    # NOTE 3. Read list
    res = client.get(API_BASE)
    assert res.status_code == 200
    lst = res.json()["data"]
    assert isinstance(lst, list)
    assert any(r["route_id"] == route_id for r in lst)

    # NOTE 4. Update (부분 수정)
    patched = {
        "route_id": route_id,
        "title": f"{payload['title']}-patched",
        "description": f"{payload['description']}-patched",
        "distance": payload["distance"] + 1000,
        "high_height": 150.0,
        "low_height": 10.0,
    }
    res = client.patch(API_BASE, json=patched)
    assert res.status_code == 200
    got = res.json()["data"]
    assert got["route_id"] == route_id
    assert got["title"] == patched["title"]
    assert got["description"] == patched["description"]
    assert got["distance"] == patched["distance"]
    assert float(got["high_height"]) == patched["high_height"]
    assert float(got["low_height"]) == patched["low_height"]

    # NOTE 5. 업데이트 결과 재검증
    res = client.get(f"{API_BASE}/{route_id}")
    assert res.status_code == 200
    got = res.json()["data"]
    assert got["title"] == patched["title"]

    # NOTE 6. Delete
    res = client.delete(f"{API_BASE}/{route_id}")
    assert res.status_code == 200
    body = res.json()
    assert body["code"] == 200
    assert body["message"] == "경로 삭제 성공"

    # NOTE 7. 삭제 후 조회 시 Not Found 매핑 확인
    res = client.get(f"{API_BASE}/{route_id}")
    assert res.status_code == 400
    body = res.json()
    assert body["code"] == 404
    assert body["message"] == "경로를 찾을 수 없습니다."


def test_read_route_not_found(client):
    invalid_id = 999999
    res = client.get(f"{API_BASE}/{invalid_id}")
    assert res.status_code == 400
    body = res.json()
    assert body["code"] == 404
    assert body["message"] == "경로를 찾을 수 없습니다."


def test_update_route_not_found(client):
    res = client.patch(
        API_BASE,
        json={"route_id": 999999, "title": "patched-title"},
    )
    assert res.status_code == 400
    body = res.json()
    assert body["code"] == 404
    assert body["message"] == "경로를 찾을 수 없습니다."


def test_delete_route_not_found(client):
    res = client.delete(f"{API_BASE}/999999")
    assert res.status_code == 400
    body = res.json()
    assert body["code"] == 404
    assert body["message"] == "경로를 찾을 수 없습니다."
