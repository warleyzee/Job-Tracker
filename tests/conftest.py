import pytest
from fastapi.testclient import TestClient

from main import app
from services.service_application import rest_storage


@pytest.fixture()
def client() -> TestClient:
    rest_storage()
    return TestClient(app)
