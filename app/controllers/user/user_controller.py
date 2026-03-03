from typing import List
from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
from app.controllers.user.serializers import AddOrUpdateUserRequest
from app.domain.models.user_data import Stock, User
from app.domain.services.user_service import UserService
from app.infrastucture.client.market_stack_api.market_stack_api import MarketStackApi
from app.infrastucture.notifier.ses_email_sender import SesEmailSender
from app.infrastucture.repository.dynamo_db_user_data_repository import DynamoDbUserDataRepository
from app.settings import Settings


settings = Settings()

api_router = APIRouter()

user_repo = DynamoDbUserDataRepository()
stock_api = MarketStackApi()
user_notifier = SesEmailSender()
user_service = UserService(user_repo, stock_api, user_notifier)


@api_router.post(
        "/addUser"
)
async def add_user(
    request: AddOrUpdateUserRequest
):  
    new_user: User = User(
        user_identifier=request.user_identifier.lower(),
        email=request.email,
        name=request.name,
        stocks=request.stocks
    )
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
    user_id: str,
    response: Response
) -> JSONResponse:
    try: 
        user_info: List[Stock] =  user_service.get_user_info(user_id)
        response.status_code = 200
        return {
            "status": "Success",
            "userInfo" : user_info
        }
    except: 
        response.status_code = 404
        return {
            "status": "Error",
            "message" : "User not found"
        }      


@api_router.patch(
        "/addOrUpdateUserStocks/{user_id}"
)
async def addOrUpdateStocksToUser(
    user_id: str,
    request: AddOrUpdateUserRequest
) -> JSONResponse:
    print("Add or update")
    user: User = User(user_identifier=user_id.lower(), stocks=request.stocks)
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


@api_router.patch(
        "/deleteUserStocks/{user_id}"
)
async def deleteUserStocksToUser(
    user_id: str,
    request: AddOrUpdateUserRequest
) -> JSONResponse:
    user: User = User(user_identifier=user_id.lower(), stocks=request.stocks)
    updated = user_service.update_user(user_to_update= user, delete=True)
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
        "/deleteUser/{user_identifier}"
)
async def delete_user(
    user_identifier: str
) -> JSONResponse:
    try: 
        user_service.delete_user(user_id = user_identifier.lower())
        return JSONResponse(
            content={"message":"User deleted correctly"},
            status_code=200
        )
    except ValueError:
        return JSONResponse(
            content={"message":"User Not Found"},
            status_code=404
        )
 