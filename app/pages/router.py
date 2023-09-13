from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.hotels.router import get_all_hotels

router = APIRouter(prefix="/pages", tags=["Frontend"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/", include_in_schema=False)
async def get_hotels_page(request: Request, hotels=Depends(get_all_hotels)):
    return templates.TemplateResponse(
        name="hotels.html", context={"request": request, "hotels": hotels}
    )
