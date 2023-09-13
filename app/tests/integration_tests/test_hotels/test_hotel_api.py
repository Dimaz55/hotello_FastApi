import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "date_from, date_to, status_code",
    [
        ("2023-07-01", "2023-07-15", 200),
        ("2023-07-15", "2023-07-01", 400),
        ("2023-07-01", "2023-07-01", 400),
        ("2023-07-01", "2023-09-01", 400),
    ],
)
async def test_get_hotels_by_location(
    date_from, date_to, status_code, ac: AsyncClient
):
    response = await ac.get(
        "/hotels/Алтай", params={"date_from": date_from, "date_to": date_to}
    )
    assert response.status_code == status_code
