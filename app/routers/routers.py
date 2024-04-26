from app.routers.users import *
from app.routers.auth import auth_router

health_router = APIRouter()


@health_router.get("/")
async def healthcheck():
    return {"status_code": "200", "detail": "ok", "result": "working"}