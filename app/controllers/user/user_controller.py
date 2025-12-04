from typing import List
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.controllers.user.serializers import AddOrUpdateUserRequest
from app.domain.models.user_data import Stock, UserPortfolio
from app.domain.services.user_service import UserService
from app.infrastucture.client.market_stack_api.market_stack_api import MarketStackApi
from app.infrastucture.repository.json_user_data_repository import JSONUserDataRepository
from app.settings import Settings


settings = Settings()

api_router = APIRouter()

user_repo = JSONUserDataRepository()
stock_api = MarketStackApi()
user_service = UserService(user_repo, stock_api)


@api_router.post(
        "/addUser"
)
async def add_user(
    request: AddOrUpdateUserRequest
):  
    new_user: UserPortfolio = UserPortfolio(name=request.name.lower(), stocks=request.stocks)
    try: 
        user_service.add_user(new_user = new_user)
        return JSONResponse(
            content={"Message": "User created successfully", "status":"Success"},
            status_code=200
        )
    except ValueError:
        return JSONResponse(
            content={"ErrorMessage": "Error creating user. Please contact our support center", "status":"Error"},
            status_code=500
        )
    
@api_router.get(
        "/getUserStocksInfo/{user_id}"
)
async def get_user_stocks_info(
    user_id: str 
) -> JSONResponse:
    user_info: List[Stock] =  user_service.get_user_info(user_id)
    return JSONResponse( 
            content={
                "status": " Success",
                "userInfo": [stock.model_dump() for stock in user_info]
            },
            status_code=200,
        )

@api_router.patch(
        "/addOrUpdateUserStocks/{user_id}"
)
async def update(
    user_id: str,
    request: AddOrUpdateUserRequest
) -> JSONResponse:
    user: UserPortfolio = UserPortfolio(name=user_id.lower(), stocks=request.stocks)
    updated = user_service.update_user(user_to_update= user)
    if updated:
        return JSONResponse( 
                content={
                    "message": "User updated",
                    "status": " Success",
                },
                status_code=200,
            )
    else: 
          return JSONResponse( 
                content={
                    "message": "User not found",
                    "status": " Error",
                },
                status_code=200,
            )      
    
@api_router.delete(
        "/deleteUser/{name}"
)
async def delete_user(
    name: str
) -> JSONResponse:
    try: 
        user_service.delete_user(user_id = name.lower())
        return JSONResponse(
            content="User deleted correctly",
            status_code=200
        )
    except ValueError:
        return JSONResponse(
            content="User Not Found",
            status_code=404
        )
 