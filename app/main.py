from contextlib import asynccontextmanager
from fastapi import FastAPI
from mangum import Mangum 
from app.controllers.user.user_controller import api_router
from app.controllers.stock.stock_controller import stock_router
from app.controllers.healtz import healtz_router
from app.infrastucture.client.dynamodb_client import create_users_table_if_not_exists


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("server is starting.")
    create_users_table_if_not_exists()
    yield
    print("server is shutting down")


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)
app.include_router(stock_router)
app.include_router(healtz_router)

handler = Mangum(app, lifespan="off")
