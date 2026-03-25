import time

import app.main as main_module
from app.database import SessionLocal
from app.models import OpportunityModel


EXPECTED_SOURCES = {
    "capacitate",
    "google",
    "conecta_empleo",
    "edx",
    "coursera",
    "khan",
    "santander",
    "unam",
    "idiomas",
    "becas",
}
ADMIN_HEADERS = {"X-Admin-Key": "test-admin-key"}


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_docs_available(client):
    response = client.get("/docs")
    assert response.status_code == 200


def test_list_opportunities_with_filters(client):
    response = client.get("/opportunities/", params={"limit": 5, "source": "khan"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 5
    if data:
        assert "id" in data[0]


def test_stats_endpoint(client):
    response = client.get("/opportunities/stats")
    assert response.status_code == 200
    payload = response.json()

    assert "total" in payload
    assert "active" in payload
    assert set(payload["by_source"].keys()) == EXPECTED_SOURCES


def test_sources_endpoint(client):
    response = client.get("/opportunities/sources")
    assert response.status_code == 200
    payload = response.json()
    assert set(payload["sources"].keys()) == EXPECTED_SOURCES


def test_scheduler_endpoint(client):
    response = client.get("/opportunities/scheduler")
    assert response.status_code == 200
    payload = response.json()
    assert "running" in payload


def test_get_opportunity_by_id(client):
    db = SessionLocal()
    try:
        row = (
            db.query(OpportunityModel)
            .filter(OpportunityModel.is_active.is_(True))
            .order_by(OpportunityModel.id.asc())
            .first()
        )
    finally:
        db.close()

    assert row is not None, "Expected at least one active opportunity in DB"

    response = client.get(f"/opportunities/{row.id}")
    assert response.status_code == 200
    assert response.json()["id"] == row.id


def test_crud_create_patch_delete(client):
    unique_suffix = int(time.time() * 1000)
    create_payload = {
        "title": "Curso de prueba CRUD",
        "description": "Registro creado para prueba",
        "opportunity_type": "course",
        "provider": "Admin",
        "source_url": f"https://example.com/crud-test-opportunity-{unique_suffix}",
        "source": "manual",
        "location": "Online",
        "is_free": True,
        "tags": ["test", "crud"],
    }

    created = client.post("/opportunities/", json=create_payload, headers=ADMIN_HEADERS)
    assert created.status_code == 201
    created_body = created.json()
    assert created_body["id"] is not None
    created_id = created_body["id"]

    patched = client.patch(
        f"/opportunities/{created_id}",
        json={"title": "Curso de prueba CRUD actualizado", "is_free": False},
        headers=ADMIN_HEADERS,
    )
    assert patched.status_code == 200
    patched_body = patched.json()
    assert patched_body["title"] == "Curso de prueba CRUD actualizado"
    assert patched_body["is_free"] is False
    assert patched_body["id"] == created_id

    deleted = client.delete(f"/opportunities/{created_id}", headers=ADMIN_HEADERS)
    assert deleted.status_code == 204

    after_delete = client.get(f"/opportunities/{created_id}")
    assert after_delete.status_code == 404


def test_crud_requires_admin_key(client):
    create_payload = {
        "title": "Curso sin credenciales",
        "opportunity_type": "course",
        "provider": "Admin",
        "source_url": f"https://example.com/no-auth-{int(time.time() * 1000)}",
    }
    response = client.post("/opportunities/", json=create_payload)
    assert response.status_code == 401


def test_invalid_refresh_source_returns_400(client):
    response = client.post(
        "/opportunities/refresh",
        params={"source": "definitely_invalid_source"},
        headers=ADMIN_HEADERS,
    )
    assert response.status_code == 400


def test_rate_limiting_window_resets(client):
    original_limit = main_module.settings.rate_limit_per_minute
    original_window = main_module.settings.rate_limit_window_seconds
    main_module.settings.rate_limit_per_minute = 1
    main_module.settings.rate_limit_window_seconds = 1
    main_module.request_counts.clear()

    try:
        first = client.get("/opportunities/stats")
        second = client.get("/opportunities/stats")
        time.sleep(1.1)
        third = client.get("/opportunities/stats")
    finally:
        main_module.settings.rate_limit_per_minute = original_limit
        main_module.settings.rate_limit_window_seconds = original_window
        main_module.request_counts.clear()

    assert first.status_code == 200
    assert second.status_code == 429
    assert third.status_code == 200
