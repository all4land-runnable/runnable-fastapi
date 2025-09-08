# test/test_pace_records.py
from uuid import uuid4

USERS_API = "/api/v1/users"
ROUTES_API = "/api/v1/routes"
CATS_API = "/api/v1/categories"
UR_API = "/api/v1/user-routes"
RECORDS_API = "/api/v1/records"
PR_API = "/api/v1/pace-records"

def _bootstrap_record(client):
    u = client.post(USERS_API, json={
        "email": f"pr+{uuid4().hex[:6]}@all4land.com",
        "password": "abcd1234",
        "username": f"pr-{uuid4().hex[:6]}",
        "age": 28, "runner_since": 2022, "pace_average": 380,
    }).json()["data"]
    r = client.post(ROUTES_API, json={
        "title": f"pr-{uuid4().hex[:4]}",
        "description": "for-pace-record",
        "distance": 3000, "high_height": 5.0, "low_height": 1.0,
    }).json()["data"]
    c = client.post(CATS_API, json={"user_id": u["user_id"], "name": "cat"}).json()["data"]
    ur = client.post(UR_API, json={"user_id": u["user_id"], "category_id": c["category_id"], "route_id": r["route_id"]}).json()["data"]
    rec = client.post(RECORDS_API, json={"user_route_id": ur["user_route_id"], "paces_average": 345}).json()["data"]
    return rec["record_id"]

def test_pace_records_crud(client):
    record_id = _bootstrap_record(client)

    # Create (section_id 생략: 모델이 nullable이므로 가능)
    res = client.post(PR_API, json={"record_id": record_id, "pace": 380})
    assert res.status_code == 201
    pr = res.json()["data"]
    pr_id = pr["pace_record_id"]

    # Read by id
    res = client.get(f"{PR_API}/{pr_id}")
    assert res.status_code == 200
    assert res.json()["data"]["pace_record_id"] == pr_id

    # Read list
    res = client.get(PR_API)
    assert res.status_code == 200
    assert any(x["pace_record_id"] == pr_id for x in res.json()["data"])

    # Read by record
    res = client.get(f"{PR_API}/record/{record_id}")
    assert res.status_code == 200
    assert any(x["pace_record_id"] == pr_id for x in res.json()["data"])

    # Update
    res = client.patch(PR_API, json={"pace_record_id": pr_id, "pace": 365})
    assert res.status_code == 200
    assert res.json()["data"]["pace"] == 365

    # Delete
    res = client.delete(f"{PR_API}/{pr_id}")
    assert res.status_code == 200
    assert res.json()["message"] == "페이스 기록 삭제 성공"
