from contextlib import asynccontextmanager
from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from app.logger import logger
from app.admin.admin import BookingAdmin, HotelAdmin, RoomAdmin, UserAdmin
from app.admin.auth import authentication_backend
from app.bookings.router import router as booking_router
from app.config import settings
from app.db import engine
from app.hotels.rooms.router import router as room_router
from app.hotels.router import router as hotel_router
from app.images.router import router as images_router
from app.middlewares import ProcessTimeMiddleware
from app.pages.router import router as pages_router
from app.users.router import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Service started")
    try:
        redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}", encoding="utf-8")
        FastAPICache.init(RedisBackend(redis), prefix="cache")
    except Exception as e:
        logger.error(f"Redis error", extra={
            "exception": e
        })
    yield
    logger.info("Service exited")


app = FastAPI(
    title="Отелло - сервис бронирования отелей", version="0.1.0", lifespan=lifespan
)
app.include_router(user_router)
app.include_router(hotel_router)
app.include_router(room_router)
app.include_router(booking_router)
app.include_router(pages_router)
app.include_router(images_router)

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS", "POST", "DELETE"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

app.add_middleware(ProcessTimeMiddleware, app_logger=logger)

admin = Admin(
    app=app,
    engine=engine,
    title="Отелло - админ панель",
    authentication_backend=authentication_backend,
)
admin.add_view(UserAdmin)
admin.add_view(BookingAdmin)
admin.add_view(HotelAdmin)
admin.add_view(RoomAdmin)

app.mount("/static", StaticFiles(directory="app/static"), "static")


@app.get('/', include_in_schema=False)
async def root():
    return RedirectResponse('/docs')
