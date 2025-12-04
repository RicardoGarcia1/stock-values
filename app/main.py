from fastapi import FastAPI
from mangum import Mangum 
from app.controllers.user.user_controller import api_router
from app.controllers.stock.stock_controller import stock_router
from app.controllers.healtz import healtz_router


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print("server is starting.")
#     await create_db_and_tables()
#     yield
#     print("server is shutting down")


#app = FastAPI(lifespan=lifespan)
app = FastAPI()
app.include_router(api_router)
app.include_router(stock_router)
app.include_router(healtz_router)

handler = Mangum(app, lifespan="off")
