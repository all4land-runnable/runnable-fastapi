# tests/test_users_crud.py
from uuid import uuid4

API_BASE = "/api/v1/users"


def _mk_user_payload():
    """
    유니크 제약(이메일/유저명) 피하기 위해 매번 다른 값 생성
    """
    return {
        "email": f"test+{uuid4().hex[:6]}@all4land.com",
        "password": "abcd1234",
        "username": f"올포랜드-{uuid4().hex[:6]}",
        "age": 28,
        "runner_since": 2022,
        "pace_average": 390,
    }


def test_create_read_update_delete_user(client):
    # NOTE 1. Create 테스트
    payload = _mk_user_payload()
    res = client.post(API_BASE, json=payload, headers={"accept": "application/json"})
    assert res.status_code == 201

    body = res.json()
    assert body["code"] == 201
    assert body["message"] == "유저 생성 성공"

    data = body["data"]
    assert data["email"] == payload["email"]
    assert data["username"] == payload["username"]
    assert "user_id" in data

    # NOTE 2. Read by id
    user_id = data["user_id"]
    res = client.get(f"{API_BASE}/{user_id}")
    assert res.status_code == 200

    got = res.json()["data"]
    assert got["user_id"] == user_id
    assert got["email"] == payload["email"]
    assert got["username"] == payload["username"]

    # NOTE 3. Read: by email
    res = client.get(f"{API_BASE}/email/{payload['email']}")
    assert res.status_code == 200

    got = res.json()["data"]
    assert got["user_id"] == user_id

    # NOTE 4. Read: by username
    res = client.get(f"{API_BASE}/username/{payload['username']}")
    assert res.status_code == 200

    got = res.json()["data"]
    assert got["user_id"] == user_id

    # NOTE 5. Read: list (전체 조회)
    res = client.get(API_BASE)
    assert res.status_code == 200

    lst = res.json()["data"]
    assert isinstance(lst, list)
    assert any(u["user_id"] == user_id for u in lst)

    # NOTE 6. Update (부분 수정)
    patched_username = f"{payload['username']}-patched"
    patch_body = {
        "user_id": user_id,
        "username": patched_username,
    }

    res = client.patch(API_BASE, json=patch_body)
    assert res.status_code == 200

    got = res.json()["data"]
    assert got["user_id"] == user_id
    assert got["username"] == patched_username

    # NOTE 7. 업데이트 결과 재검증 (by id)
    res = client.get(f"{API_BASE}/{user_id}")
    assert res.status_code == 200

    got = res.json()["data"]
    assert got["username"] == patched_username

    # NOTE 8. Delete
    res = client.delete(f"{API_BASE}/{user_id}")
    assert res.status_code == 200

    body = res.json()
    assert body["code"] == 200
    assert body["message"] == "유저 삭제 성공"


def test_create_duplicate_username_should_fail(client):
    p1 = _mk_user_payload()
    res = client.post(API_BASE, json=p1)
    assert res.status_code == 201

    p2 = _mk_user_payload()
    p2["username"] = p1["username"]  # username만 중복
    res = client.post(API_BASE, json=p2)

    assert res.status_code == 400  # 전역 핸들러 맵핑에 맞춰 400 권장

    body = res.json()
    assert body["code"] == 404
    assert body["message"] == "중복된 이메일/사용자명 입니다."

