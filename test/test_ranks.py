from uuid import uuid4

USERS_API = "/api/v1/users"
ROUTES_API = "/api/v1/routes"
CATS_API = "/api/v1/categories"
UR_API = "/api/v1/user-routes"
RECORDS_API = "/api/v1/records"
RANKS_API = "/api/v1/ranks"

def _bootstrap_record(client):
    u = client.post(USERS_API, json={
        "email": f"rk+{uuid4().hex[:6]}@all4land.com",
        "password": "abcd1234",
        "username": f"rk-{uuid4().hex[:6]}",
        "age": 28, "runner_since": 2022, "pace_average": 380,
    }).json()["data"]
    r = client.post(ROUTES_API, json={
        "title": f"rk-{uuid4().hex[:4]}",
        "description": "for-rank",
        "distance": 5000, "high_height": 10.0, "low_height": 2.0,
    }).json()["data"]
    c = client.post(CATS_API, json={"user_id": u["user_id"], "name": "cat"}).json()["data"]
    ur = client.post(UR_API, json={"user_id": u["user_id"], "category_id": c["category_id"], "route_id": r["route_id"]}).json()["data"]
    rec = client.post(RECORDS_API, json={"user_route_id": ur["user_route_id"], "paces_average": 360}).json()["data"]
    return rec["record_id"]

def test_ranks_crud(client):
    record_id = _bootstrap_record(client)

    # Create
    res = client.post(RANKS_API, json={"record_id": record_id, "rank": 5})
    assert res.status_code == 201
    rk = res.json()["data"]
    rank_id = rk["rank_id"]

    # Read by id
    res = client.get(f"{RANKS_API}/{rank_id}")
    assert res.status_code == 200
    assert res.json()["data"]["rank_id"] == rank_id

    # Read list
    res = client.get(RANKS_API)
    assert res.status_code == 200
    assert any(x["rank_id"] == rank_id for x in res.json()["data"])

    # Read by record
    res = client.get(f"{RANKS_API}/record/{record_id}")
    assert res.status_code == 200
    assert any(x["rank_id"] == rank_id for x in res.json()["data"])

    # Update
    res = client.patch(RANKS_API, json={"rank_id": rank_id, "rank": 3})
    assert res.status_code == 200
    assert res.json()["data"]["rank"] == 3

    # Delete
    res = client.delete(f"{RANKS_API}/{rank_id}")
    assert res.status_code == 200
    assert res.json()["message"] == "랭크 삭제 성공"
