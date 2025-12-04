from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.settings import Settings


settings = Settings()

healtz_router = APIRouter()


@healtz_router.get("/healtz")
async def healtz() -> JSONResponse:
    return JSONResponse(content={"status": "200", "message": "OK"}, status_code=200)
