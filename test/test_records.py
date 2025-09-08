# test/test_records.py
from uuid import uuid4

USERS_API = "/api/v1/users"
ROUTES_API = "/api/v1/routes"
CATS_API = "/api/v1/categories"
UR_API = "/api/v1/user-routes"
RECORDS_API = "/api/v1/records"

def _mk_user():
    return {
        "email": f"rec+{uuid4().hex[:6]}@all4land.com",
        "password": "abcd1234",
        "username": f"rec-{uuid4().hex[:6]}",
        "age": 28, "runner_since": 2022, "pace_average": 380,
    }

def _mk_route():
    return {
        "title": f"r-{uuid4().hex[:4]}",
        "description": "for-record",
        "distance": 10000, "high_height": 123.4, "low_height": 12.3,
    }

def _mk_category(user_id: int):
    return {"user_id": user_id, "name": f"cat-{uuid4().hex[:4]}"}

def _link_user_route(user_id: int, category_id: int, route_id: int):
    return {"user_id": user_id, "category_id": category_id, "route_id": route_id}

def _mk_record(user_route_id: int):
    return {"user_route_id": user_route_id, "paces_average": 385}

def test_records_crud(client):
    u = client.post(USERS_API, json=_mk_user()).json()["data"]
    r = client.post(ROUTES_API, json=_mk_route()).json()["data"]
    c = client.post(CATS_API, json=_mk_category(u["user_id"])).json()["data"]
    ur = client.post(UR_API, json=_link_user_route(u["user_id"], c["category_id"], r["route_id"])).json()["data"]

    # Create
    res = client.post(RECORDS_API, json=_mk_record(ur["user_route_id"]))
    assert res.status_code == 201
    rec = res.json()["data"]
    rec_id = rec["record_id"]

    # Read by id
    res = client.get(f"{RECORDS_API}/{rec_id}")
    assert res.status_code == 200
    assert res.json()["data"]["record_id"] == rec_id

    # Read list
    res = client.get(RECORDS_API)
    assert res.status_code == 200
    assert any(x["record_id"] == rec_id for x in res.json()["data"])

    # Read by user_route
    res = client.get(f"{RECORDS_API}/user-route/{ur['user_route_id']}")
    assert res.status_code == 200
    assert any(x["record_id"] == rec_id for x in res.json()["data"])

    # Update
    patch = {"record_id": rec_id, "paces_average": 370}
    res = client.patch(RECORDS_API, json=patch)
    assert res.status_code == 200
    assert res.json()["data"]["paces_average"] == 370

    # Delete
    res = client.delete(f"{RECORDS_API}/{rec_id}")
    assert res.status_code == 200
    assert res.json()["message"] == "기록 삭제 성공"
