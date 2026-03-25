import pytest
from fastapi.testclient import TestClient

import app.main as main_module


@pytest.fixture
def client(monkeypatch):
    """Create a test client with scheduler side effects disabled."""
    monkeypatch.setattr(main_module, "start_scheduler", lambda interval_hours=6: None)
    monkeypatch.setattr(main_module, "stop_scheduler", lambda: None)
    monkeypatch.setattr(main_module.settings, "admin_api_key", "test-admin-key")
    main_module.request_counts.clear()

    with TestClient(main_module.app) as test_client:
        yield test_client
