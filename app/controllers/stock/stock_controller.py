from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.domain.services.user_service import UserService
from app.infrastucture.client.market_stack_api.market_stack_api import MarketStackApi
from app.infrastucture.notifier.ses_email_sender import SesEmailSender
from app.infrastucture.repository.dynamo_db_user_data_repository import DynamoDbUserDataRepository
from app.settings import Settings


settings = Settings()

stock_router = APIRouter()

user_repo = DynamoDbUserDataRepository()
stock_api = MarketStackApi()
user_notifier = SesEmailSender()
user_service = UserService(user_repo, stock_api,user_notifier)

   
@stock_router.get(
        "/getCurrentEndOfTheDayTotalAmount/{user_id}"
)
async def get_current_total_balance_eof(
    user_id: str 
) -> JSONResponse:
    user_stocks_value =  await user_service.get_user_current_value(user_id)
    return JSONResponse( 
            content={
                "status": " Success",
                "stocksValue": user_stocks_value.get("user_current_stocks_value"),
                "totalValue": user_stocks_value.get("total", 0)
            },
            status_code=200,
        )