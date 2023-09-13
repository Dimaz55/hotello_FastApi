from sqladmin import ModelView

from app.bookings.models import Booking
from app.hotels.models import Hotel
from app.hotels.rooms.models import Room
from app.users.models import User


class UserAdmin(ModelView, model=User):
    column_exclude_list = [User.hashed_password, User.bookings]
    form_excluded_columns = [User.hashed_password]
    column_details_exclude_list = [User.hashed_password]
    can_delete = False
    column_labels = {"id": "№", "email": "Адрес"}
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class BookingAdmin(ModelView, model=Booking):
    column_list = "__all__"
    # column_exclude_list = []
    # form_excluded_columns = []
    can_delete = False
    # column_details_exclude_list = []
    name = "Бронирование"
    name_plural = "Бронирования"
    icon = "fa-solid fa-book"


class HotelAdmin(ModelView, model=Hotel):
    column_exclude_list = [Hotel.rooms, Hotel.image_id]
    can_delete = False
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"


class RoomAdmin(ModelView, model=Room):
    column_list = "__all__"
    can_delete = False
    name = "Номер"
    name_plural = "Номера"
    icon = "fa-solid fa-bed"
    form_ajax_refs = {
        "bookings": {"fields": ("id",)},
        "hotel": {"fields": ("id", "name")},
    }
