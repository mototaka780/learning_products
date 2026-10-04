# tests/test_companies.py
from uuid import UUID

def test_create_company(client):
    payload = {
        "company_name": "Test Corp",
        "industry": "IT",
        "city": "Tokyo",
        "country": "Japan",
        "employee_count": 100,
        "website": "https://example.com",
        "notes": "Test notes"
    }

    response = client.post("/companies", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["company_name"] == "Test Corp"
    assert UUID(data["id"])  # UUID 形式チェック


def test_get_companies(client):
    # まず 1 件作成
    client.post("/companies", json={
        "company_name": "A Corp",
        "industry": "IT",
        "city": "Tokyo",
        "country": "Japan",
        "employee_count": 10,
        "website": "https://a.com",
        "notes": "A"
    })

    response = client.get("/companies")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_get_company_by_id(client):
    # 作成
    create_res = client.post("/companies", json={
        "company_name": "B Corp",
        "industry": "Finance",
        "city": "Osaka",
        "country": "Japan",
        "employee_count": 50,
        "website": "https://b.com",
        "notes": "B"
    })
    company_id = create_res.json()["id"]

    # 取得
    response = client.get(f"/companies/{company_id}")
    assert response.status_code == 200
    assert response.json()["company_name"] == "B Corp"


def test_update_company(client):
    # 作成
    create_res = client.post("/companies", json={
        "company_name": "C Corp",
        "industry": "Retail",
        "city": "Nagoya",
        "country": "Japan",
        "employee_count": 20,
        "website": "https://c.com",
        "notes": "C"
    })
    company_id = create_res.json()["id"]

    # 更新
    update_res = client.put(f"/companies/{company_id}", json={
        "company_name": "C Corp Updated",
        "industry": "Retail",
        "city": "Nagoya",
        "country": "Japan",
        "employee_count": 25,
        "website": "https://c.com",
        "notes": "Updated"
    })

    assert update_res.status_code == 200
    assert update_res.json()["employee_count"] == 25


def test_delete_company(client):
    # 作成
    create_res = client.post("/companies", json={
        "company_name": "D Corp",
        "industry": "IT",
        "city": "Kyoto",
        "country": "Japan",
        "employee_count": 5,
        "website": "https://d.com",
        "notes": "D"
    })

    print("STATUS:", create_res.status_code)
    print("BODY:", create_res.json())

    company_id = create_res.json()["id"]

    # 削除
    delete_res = client.delete(f"/companies/{company_id}")
    assert delete_res.status_code == 204

    # 再取得 → 404
    get_res = client.get(f"/companies/{company_id}")
    assert get_res.status_code == 404


def test_admin_all_companies(client):
    # admin なので全件取得可能
    response = client.get("/companies/admin/all")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
