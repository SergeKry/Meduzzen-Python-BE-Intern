from app.routers.users import *

health_router = APIRouter()


@health_router.get("/")
async def healthcheck():
    return {"status_code": "200", "detail": "ok", "result": "working"}