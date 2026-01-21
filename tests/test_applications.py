from fastapi.testclient import TestClient


def test_create_application_fails_when_company_empty(client: TestClient) -> None:
    payload = {"company": "", "role": "Backend Engeneer", "status": "applied"}

    resp = client.post("/applications", json=payload)

    assert resp.status_code == 422


def test_create_application_fails_when_role_is_blank(client: TestClient) -> None:
    payload = {
        "company": "Stripe",
        "role": "   ",
        "status": "applied",
    }

    resp = client.post("/applications", json=payload)

    assert resp.status_code == 422


def test_create_application_returns_201_and_expected_json(client: TestClient) -> None:
    payload = {
        "company": "Stripe",
        "role": "Backend Engineer",
        "status": "applied",
    }

    resp = client.post("/applications", json=payload)

    assert resp.status_code == 201
    data = resp.json()

    assert "id" in data
    assert data["company"] == "Stripe"
    assert data["role"] == "Backend Engineer"
    assert data["status"] == "applied"
    assert "applied_date" in data


def test_list_applicaiton_returns_array(client: TestClient) -> None:

    resp = client.get("/applications")
    assert resp.status_code == 200
    assert resp.json() == []

    # create 1
    client.post(
        "/applications", json={"company": "Google", "role": "SRE", "status": "applied"}
    )

    resp2 = client.get("/applications")
    assert resp2.status_code == 200
    data = resp2.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["company"] == "Google"


def test_get_by_id_returns_200_and_correct_item(client: TestClient) -> None:
    create_resp = client.post(
        "/applications",
        json={"company": "Amazon", "role": "DevOps", "status": "applied"},
    )
    app_id = create_resp.json()["id"]

    resp = client.get(f"/applications/{app_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == app_id
    assert data["company"] == "Amazon"


def test_get_by_id_returns_404_when_not_found(client: TestClient) -> None:
    fake_id = "00000000-0000-0000-0000-000000000000"
    resp = client.get(f"/applications/{fake_id}")

    assert resp.status_code == 404
    assert resp.json()["detail"] == "Application not Found"
