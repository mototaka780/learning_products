
from uuid import uuid4

import pytest
from main import app
from routers.projects import get_current_user as get_projects_current_user


@pytest.fixture
def projects_client(client):
    """案件APIの認証だけをテスト用に上書きする。"""
    app.dependency_overrides[get_projects_current_user] = lambda: {
        "id": "00000000-0000-0000-0000-000000000000",
        "username": "test_user",
        "role": "admin",
    }

    try:
        yield client
    finally:
        app.dependency_overrides.pop(get_projects_current_user, None)


def create_test_company(client, company_name="Project Test Corp"):
    """案件の外部キー制約を満たすテスト用企業を作成する。"""
    response = client.post(
        "/companies",
        json={
            "company_name": company_name,
            "industry": "IT",
            "city": "Tokyo",
            "country": "Japan",
            "employee_count": 10,
            "website": "https://example.com",
            "notes": "Project test",
        },
    )
    assert response.status_code == 201, response.text
    return response.json()["id"]


def create_project_payload(company_id, project_name="Test Project"):
    return {
        "project_name": project_name,
        "project_type": "AI",
        "budget": 1000000,
        "description": "Project API test",
        "start_date": "2026-01-01",
        "end_date": "2026-12-31",
        "status": "ongoing",
        "company_id": company_id,
    }


def create_test_project(client, company_id, project_name="Test Project"):
    response = client.post(
        "/projects/",
        json=create_project_payload(company_id, project_name),
    )
    assert response.status_code == 200, response.text
    return response.json()


def test_projects_requires_authentication(client):
    response = client.get("/projects/")
    assert response.status_code == 401


def test_create_project(projects_client):
    company_id = create_test_company(projects_client)
    payload = create_project_payload(company_id)

    response = projects_client.post("/projects/", json=payload)

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["project_name"] == "Test Project"
    assert data["project_type"] == "AI"
    assert data["company_id"] == company_id
    assert data["budget"] == 1000000
    assert data["status"] == "ongoing"
    assert data["id"]
    assert data["created_at"]
    assert data["updated_at"]


def test_get_projects(projects_client):
    company_id = create_test_company(projects_client)
    create_test_project(projects_client, company_id)

    response = projects_client.get("/projects/")

    assert response.status_code == 200, response.text
    assert isinstance(response.json(), list)
    assert any(
        project["project_name"] == "Test Project"
        for project in response.json()
    )


def test_get_project_by_id(projects_client):
    company_id = create_test_company(projects_client)
    project = create_test_project(projects_client, company_id)

    response = projects_client.get(f"/projects/{project['id']}")

    assert response.status_code == 200, response.text
    assert response.json()["id"] == project["id"]
    assert response.json()["project_name"] == "Test Project"


def test_get_projects_by_company(projects_client):
    company_id = create_test_company(projects_client, "Company A")
    other_company_id = create_test_company(projects_client, "Company B")

    create_test_project(projects_client, company_id, "Company A Project")
    create_test_project(projects_client, other_company_id, "Company B Project")

    response = projects_client.get(f"/projects/company/{company_id}")

    assert response.status_code == 200, response.text
    data = response.json()
    assert all(item["company_id"] == company_id for item in data)
    assert any(item["project_name"] == "Company A Project" for item in data)
    assert all(item["project_name"] != "Company B Project" for item in data)


def test_update_project(projects_client):
    company_id = create_test_company(projects_client)
    project = create_test_project(projects_client, company_id)

    payload = create_project_payload(company_id, "Updated Project")
    payload["budget"] = 2000000
    payload["status"] = "completed"

    response = projects_client.put(
        f"/projects/{project['id']}",
        json=payload,
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["project_name"] == "Updated Project"
    assert data["budget"] == 2000000
    assert data["status"] == "completed"


def test_delete_project(projects_client):
    company_id = create_test_company(projects_client)
    project = create_test_project(projects_client, company_id)

    response = projects_client.delete(f"/projects/{project['id']}")

    assert response.status_code == 200, response.text
    assert response.json()["detail"] == "Project deleted"

    get_response = projects_client.get(f"/projects/{project['id']}")
    assert get_response.status_code == 404


def test_get_nonexistent_project_returns_404(projects_client):
    response = projects_client.get(f"/projects/{uuid4()}")

    assert response.status_code == 404


def test_update_nonexistent_project_returns_404(projects_client):
    company_id = create_test_company(projects_client)
    payload = create_project_payload(company_id)

    response = projects_client.put(
        f"/projects/{uuid4()}",
        json=payload,
    )

    assert response.status_code == 404


def test_delete_nonexistent_project_returns_404(projects_client):
    response = projects_client.delete(f"/projects/{uuid4()}")

    assert response.status_code == 404
