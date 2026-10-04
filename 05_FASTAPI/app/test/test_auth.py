# tests/test_auth.py
def test_register(client):
    payload = {
        "username": "new_user",
        "password": "password123",
        "role": "user"
    }

    response = client.post("/auth/register", json=payload)

    print("STATUS:", response.status_code)
    print("BODY:", response.json())

    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert data["username"] == "new_user"
    assert data["role"] == "user"
    
def test_login_success(client):
    # まず登録
    client.post("/auth/register", json={
        "username": "login_user",
        "password": "password123",
        "role": "user"
    })

    # ログイン
    response = client.post("/auth/login", json={
        "username": "login_user",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_fail(client):
    response = client.post("/auth/login", json={
        "username": "unknown",
        "password": "wrong"
    })
    assert response.status_code == 401


def test_me(client):
    # FakeUser を返すよう override している
    response = client.get("/auth/me")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "test_user"
    assert data["role"] == "admin"
