from datetime import datetime

from app.bookings.models import Booking
from app.bookings.repo import BookingRepo


async def test_add_and_get_booking_repo():
    new_booking: Booking = await BookingRepo.add(
        user_id=1,
        room_id=1,
        date_from=datetime.strptime("2023-07-01", "%Y-%m-%d"),
        date_to=datetime.strptime("2023-07-15", "%Y-%m-%d"),
    )

    assert new_booking.user_id == 1
    assert new_booking.room_id == 1

    res: Booking = await BookingRepo.find_by_id(new_booking.id)
    assert res.id == new_booking.id


async def test_delete_booking():
    await BookingRepo.delete_one(user_id=1, booking_id=11)
    booking = await BookingRepo.find_by_id(11)
    assert booking is None
