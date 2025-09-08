# test/test_sections.py
from uuid import uuid4

ROUTES_API = "/api/v1/routes"
SECTIONS_API = "/api/v1/sections"


def _mk_route_payload():
    # 섹션은 route FK가 필요 → 먼저 route 생성
    return {
        "title": f"테스트루트-{uuid4().hex[:6]}",
        "description": "테스트용 경로",
        "distance": 5000,         # 5km
        "high_height": 123.4,
        "low_height": 12.3,
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
        "slope": 3,  # TODO: 타입 변경 시 테스트도 조정
    }


def test_sections_crud(client):
    # 1) Route 생성
    r_payload = _mk_route_payload()
    r_res = client.post(ROUTES_API, json=r_payload)
    assert r_res.status_code == 201
    route_id = r_res.json()["data"]["route_id"]

    # 2) Section 생성
    s_payload = _mk_section_payload(route_id)
    res = client.post(SECTIONS_API, json=s_payload)
    assert res.status_code == 201
    body = res.json()
    assert body["code"] == 201
    assert body["message"] == "섹션 생성 성공"

    data = body["data"]
    section_id = data["section_id"]
    assert data["route_id"] == route_id
    assert data["slope"] == s_payload["slope"]

    # 3) 개별 조회
    res = client.get(f"{SECTIONS_API}/{section_id}")
    assert res.status_code == 200
    got = res.json()["data"]
    assert got["section_id"] == section_id
    assert got["route_id"] == route_id

    # 4) route_id로 조회
    res = client.get(f"{SECTIONS_API}/route/{route_id}")
    assert res.status_code == 200
    lst = res.json()["data"]
    assert any(s["section_id"] == section_id for s in lst)

    # 5) 전체 조회
    res = client.get(SECTIONS_API)
    assert res.status_code == 200
    lst = res.json()["data"]
    assert isinstance(lst, list)
    assert any(s["section_id"] == section_id for s in lst)

    # 6) 부분 수정
    patched = {
        "section_id": section_id,
        "end_height": 21.0,
        "slope": 5,
    }
    res = client.patch(SECTIONS_API, json=patched)
    assert res.status_code == 200
    got = res.json()["data"]
    assert got["section_id"] == section_id
    assert got["end_height"] == 21.0
    assert got["slope"] == 5

    # 7) 삭제
    res = client.delete(f"{SECTIONS_API}/{section_id}")
    assert res.status_code == 200
    assert res.json()["message"] == "섹션 삭제 성공"

    # 8) 삭제 후 조회 → 400 + SECTION_NOT_FOUND
    res = client.get(f"{SECTIONS_API}/{section_id}")
    assert res.status_code == 400
    body = res.json()
    assert body["code"] == 404
    assert body["message"] == "섹션을 찾을 수 없습니다."
