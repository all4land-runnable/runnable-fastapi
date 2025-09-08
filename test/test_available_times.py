# tests/test_available_times_crud.py
from datetime import datetime, timedelta, timezone
from uuid import uuid4

ROUTES_API = "/api/v1/routes"
AT_API = "/api/v1/available-times"

def _mk_route_payload():
    return {
        "title": f"루트-{uuid4().hex[:6]}",
        "description": "테스트 루트",
        "distance": 10000,
        "high_height": 111.1,
        "low_height": 11.1,
    }

def _mk_available_time_payload(route_id: int):
    now = datetime.now(timezone.utc).replace(microsecond=0)
    return {
        "route_id": route_id,
        "since": (now).isoformat(),
        "start_time": (now + timedelta(hours=1)).isoformat(),
        "end_time": (now + timedelta(hours=3)).isoformat(),
    }

def _create_route(client) -> int:
    res = client.post(ROUTES_API, json=_mk_route_payload())
    assert res.status_code == 201
    return res.json()["data"]["route_id"]

def test_create_read_update_delete_available_time(client):
    # 준비: route 생성
    route_id = _create_route(client)

    # NOTE 1. Create
    payload = _mk_available_time_payload(route_id)
    res = client.post(AT_API, json=payload, headers={"accept": "application/json"})
    assert res.status_code == 201

    body = res.json()
    assert body["code"] == 201
    assert body["message"] == "이용 가능 시간 생성 성공"

    data = body["data"]
    at_id = data["available_time_id"]
    assert data["route_id"] == route_id

    # NOTE 2. Read by id
    res = client.get(f"{AT_API}/{at_id}")
    assert res.status_code == 200
    got = res.json()["data"]
    assert got["available_time_id"] == at_id

    # NOTE 3. Read list
    res = client.get(AT_API)
    assert res.status_code == 200
    lst = res.json()["data"]
    assert isinstance(lst, list)
    assert any(x["available_time_id"] == at_id for x in lst)

    # NOTE 4. Read by route_id
    res = client.get(f"{AT_API}/route/{route_id}")
    assert res.status_code == 200
    lst = res.json()["data"]
    assert any(x["available_time_id"] == at_id for x in lst)

    # NOTE 5. Update (시간 조정)
    patch_body = {
        "available_time_id": at_id,
        "end_time": (datetime.fromisoformat(payload["end_time"]) + timedelta(hours=1)).isoformat(),
    }
    res = client.patch(AT_API, json=patch_body)
    assert res.status_code == 200
    got = res.json()["data"]
    assert got["available_time_id"] == at_id
    assert got["end_time"] == patch_body["end_time"]

    # NOTE 6. Delete
    res = client.delete(f"{AT_API}/{at_id}")
    assert res.status_code == 200
    body = res.json()
    assert body["code"] == 200
    assert body["message"] == "이용 가능 시간 삭제 성공"

    # NOTE 7. 삭제 후 조회는 Not Found
    res = client.get(f"{AT_API}/{at_id}")
    assert res.status_code == 400
    body = res.json()
    assert body["code"] == 404
    assert body["message"] == "이용 가능 시간을 찾을 수 없습니다."
