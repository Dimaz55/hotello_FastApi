from pprint import pprint

import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code, booked_rooms",
    *[
        [(4, "2030-05-01", "2030-05-15", 200, i) for i in range(2, 10)]
        + [(4, "2030-05-01", "2030-05-15", 409, 9)] * 2
    ],
)
async def test_add_and_get_booking(
    room_id,
    date_from,
    date_to,
    status_code,
    booked_rooms,
    authenticated_ac: AsyncClient,
    prepare_db,
):
    res = await authenticated_ac.post(
        "/bookings",
        params={"room_id": room_id, "date_from": date_from, "date_to": date_to},
    )
    assert res.status_code == status_code

    res = await authenticated_ac.get("/bookings")
    assert len(res.json()) == booked_rooms


async def test_get_and_delete_all_booking(authenticated_ac: AsyncClient):
    res = await authenticated_ac.get("/bookings")
    bookings_json = res.json()
    assert len(bookings_json) > 0

    id_list = [str(booking["id"]) for booking in bookings_json]

    for booking_id in id_list:
        res = await authenticated_ac.delete(f"/bookings/{booking_id}")
        assert res.status_code == 204

    res = await authenticated_ac.get("/bookings")
    bookings_json = res.json()
    assert len(bookings_json) == 0
