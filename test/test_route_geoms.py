# tests/test_route_geoms_crud.py
from uuid import uuid4

ROUTES_API = "/api/v1/routes"
ROUTE_GEOMS_API = "/api/v1/route-geoms"

def _mk_route_payload():
    return {
        "title": f"테스트루트-{uuid4().hex[:6]}",
        "description": "테스트용 경로",
        "distance": 5000,
        "high_height": 123.4,
        "low_height": 12.3,
    }

def _mk_route_geom_payload(route_id: int):
    # 예: GeoJSON 문자열 또는 WKT 문자열. 여기선 단순 문자열로 저장.
    return {
        "route_id": route_id,
        "geom": '{"type":"LineString","coordinates":[[127.0,37.5],[127.01,37.51]]}',
    }

def test_route_geoms_crud(client):
    # 1) 선행: route 생성
    r = client.post(ROUTES_API, json=_mk_route_payload())
    assert r.status_code == 201
    route_id = r.json()["data"]["route_id"]

    # 2) Create
    payload = _mk_route_geom_payload(route_id)
    res = client.post(ROUTE_GEOMS_API, json=payload)
    assert res.status_code == 201
    body = res.json()
    assert body["code"] == 201
    assert body["data"]["route_id"] == route_id
    route_geom_id = body["data"]["route_geom_id"]

    # 3) Read by id
    res = client.get(f"{ROUTE_GEOMS_API}/{route_geom_id}")
    assert res.status_code == 200
    got = res.json()["data"]
    assert got["route_geom_id"] == route_geom_id
    assert got["geom"] == payload["geom"]

    # 4) Read by route_id
    res = client.get(f"{ROUTE_GEOMS_API}/route/{route_id}")
    assert res.status_code == 200
    lst = res.json()["data"]
    assert any(x["route_geom_id"] == route_geom_id for x in lst)

    # 5) Read all
    res = client.get(ROUTE_GEOMS_API)
    assert res.status_code == 200
    lst = res.json()["data"]
    assert isinstance(lst, list)
    assert any(x["route_geom_id"] == route_geom_id for x in lst)

    # 6) Update
    patched = {
        "route_geom_id": route_geom_id,
        "geom": '{"type":"LineString","coordinates":[[127.002,37.502],[127.012,37.512]]}',
    }
    res = client.patch(ROUTE_GEOMS_API, json=patched)
    assert res.status_code == 200
    got = res.json()["data"]
    assert got["route_geom_id"] == route_geom_id
    assert got["geom"] == patched["geom"]

    # 7) Delete
    res = client.delete(f"{ROUTE_GEOMS_API}/{route_geom_id}")
    assert res.status_code == 200
    assert res.json()["message"] == "경로 지오메트리 삭제 성공"

    # 8) 삭제 후 조회 → 400 + ROUTE_GEOM_NOT_FOUND
    res = client.get(f"{ROUTE_GEOMS_API}/{route_geom_id}")
    assert res.status_code == 400
    body = res.json()
    assert body["code"] == 404
    assert body["message"] == "경로 지오메트리를 찾을 수 없습니다."
