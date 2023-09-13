import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("abc@def.com", "pass1", 201),
        ("abc@def.com", "pass2", 409),
        ("not-email", "pass", 422),
    ],
)
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/auth/register", json={"email": email, "password": password}
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("user@example.com", "string", 200),
        ("not@exist.com", "pass", 401),
        ("not-email", "pass", 422),
    ],
)
async def test_login_user(email, password, status_code, ac: AsyncClient):
    res = await ac.post(
        "/auth/login", json={"email": email, "password": password}
    )
    assert res.status_code == status_code
