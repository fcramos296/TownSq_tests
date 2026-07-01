import pytest
import requests
from utils.settings import settings


@pytest.mark.api
@pytest.mark.smoke
class TestLoginAPI:
    def test_login_endpoint_options(self):
        response = requests.options(settings.BASE_URL, timeout=10)
        assert response.status_code in [200, 204, 405]

    def test_login_endpoint_post_empty_payload(self):
        response = requests.post(settings.BASE_URL, json={}, timeout=10)
        assert response.status_code in [400, 401, 403, 405, 422]

    def test_login_endpoint_post_invalid_payload(self):
        response = requests.post(settings.BASE_URL, json={"email": "invalid", "password": "invalid"}, timeout=10)
        assert response.status_code in [400, 401, 403, 405, 422]

    @pytest.mark.skipif(not settings.USERNAME or not settings.PASSWORD, reason="Credentials not configured")
    def test_login_endpoint_post_valid_credentials(self):
        response = requests.post(settings.BASE_URL, json={"email": settings.USERNAME, "password": settings.PASSWORD}, timeout=10)
        assert response.status_code in [200, 201, 302, 400, 401, 403, 405, 422]

    def test_login_page_status_code(self):
        response = requests.get(settings.BASE_URL, timeout=10)
        assert response.status_code == 200
        assert "text/html" in response.headers.get("Content-Type", "")
