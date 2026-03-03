from typing import List
from app.domain.models.user_data import Stock, User
from app.domain.ports.email_sender_port import EmailSenderPort
from app.domain.ports.stock_api_port import StockApiPort
from app.domain.ports.user_data_repository_port import UserDataRepositoryPort


class UserService:
    def __init__(
            self,
            user_repo: UserDataRepositoryPort, 
            stock_api: StockApiPort,
            user_notifier: EmailSenderPort
        ):
        self.user_repo : UserDataRepositoryPort= user_repo
        self.stock_api = stock_api
        self.user_notifier: EmailSenderPort = user_notifier
        


    def add_user(self, new_user: User) -> str:
        self.user_repo.add_user(new_user = new_user)


    def get_user_info(self, user_id: str) -> List[Stock]: 
        stocks_to_retrieve : List[Stock] = self.user_repo.get_stocks_by_user(user_id=user_id)
        print(f"stocks to retrieve: {stocks_to_retrieve}")
        return stocks_to_retrieve


    def delete_user(self, user_id: str):
        self.user_repo.delete_user(user_id = user_id)


    def update_user(self, user_to_update: User, delete: bool = False):
        return self.user_repo.patch_user(user_to_update = user_to_update, delete = delete)


    async def get_user_current_value(self, user_id: str):
        stocks_to_retrieve : List[Stock] = self.user_repo.get_stocks_by_user(user_id=user_id)
        response: List = []
        for stock in stocks_to_retrieve:
            value : float = await self.stock_api.get_price_eof(stock.index)
            print(f"Adding {stock.index} with close value {round(float(stock.amount),2)} {stock.currency.value} and amount {stock.amount}")
            response.append({"value":round(float(stock.amount),2) * value,"index":stock.index})
        
        total = sum(item.get("value", 0) for item in response)

        self.user_repo.add_or_update_history_record(total = str(total), user_id=user_id)

        name, email, user_history = self.user_repo.get_user_email_and_history(user_id= user_id)
        self.user_notifier.send_email(total = str(total), name = name , email=email, user_history = user_history)
        return {"user_current_stocks_value": response, "total":total}
