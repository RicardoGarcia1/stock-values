from decimal import Decimal
from typing import List
from app.domain.models.user_data import Currency, History, Stock, User
from app.domain.ports.user_data_repository_port import UserDataRepositoryPort
from datetime import date
from app.infrastucture.client.dynamodb_client import dynamodb
from botocore.exceptions import ClientError

class DynamoDbUserDataRepository(UserDataRepositoryPort):
    def __init__(self):
        self.table = dynamodb.Table("users")


    def _get_item(self, user_id: str):
        response = self.table.get_item(Key={"user_identifier": user_id})
        if "Item" not in response:
            return None
        user_item = response["Item"]
        return user_item
    
    
    def _put_item(self, new_user: User):
        self.table.put_item(Item=new_user.model_dump(exclude_none=True))
    
    
    def _delete_item(self, user_id: str ):
        self.table.delete_item(Key={"user_identifier": user_id})

    
    def _update_item(self, user_id: str, parameter:str, value:dict ):
        self.table.update_item(
            Key={"user_identifier": user_id},
            UpdateExpression=f"SET {parameter} = :{parameter}",
            ExpressionAttributeValues={
                f":{parameter}": value
            }
        )


    def add_user(self, new_user: User):
        try:
            if self._get_item(user_id=new_user.user_identifier) is not None:
                raise ValueError(f"User '{new_user.user_identifier}' already exists")
            self._put_item(new_user=new_user)
        except ClientError as e:
            print(f"Error al acceder a DynamoDB: {e}")
            raise


    def get_stocks_by_user(self, user_id: str) -> List[Stock]:
        if item := self._get_item(user_id=user_id):
            stocks = []
            for s in item.get("stocks"):
                amount = float(s["amount"])
                stock = Stock(
                    index=s["index"],
                    amount=Decimal(amount),
                    currency=Currency(s['currency']) if 'currency' in s else Currency.EUR
                )
                stocks.append(stock)
            return stocks
        raise "User not found"


    def delete_user(self, user_id:str):
        if self._get_item(user_id=user_id) is None:
            raise ValueError("User does not exist")
        self._delete_item(user_id=user_id)
   
   
    def patch_user(self, user_to_update: User, delete: bool = False):
        user_item = self._get_item(user_id=user_to_update.user_identifier)
        
        original_stocks = user_item.get("stocks", [])
        original_stock_dict = {
            stock["index"]: stock for stock in original_stocks
        }

        for stock in user_to_update.stocks:
            stock_dict = stock.model_dump()
            index = stock_dict["index"]
            if index in original_stock_dict:
                if delete: 
                    del original_stock_dict[index]
                else:
                    print(stock_dict)
                    original_stock_dict[index].update(stock_dict)
            elif not delete :
                original_stock_dict[index] = stock_dict

        self._update_item(user_id=user_to_update.user_identifier,
                          parameter="stocks",
                          value=list(original_stock_dict.values())
                          )

        return True


    def add_or_update_history_record(self, total:str, user_id:str):
        user_item = self._get_item(user_id=user_id)
        original_history = user_item.get("history", [])
        original_history_dict = {
            history["day"]: history["totalValue"] for history in original_history
        }
        history_to_update_list_dict : dict = []
        current_date = date.today().isoformat()
        if len(original_history_dict) == 0: 
            history_update = History(day=current_date,totalValue=total)  
            history_to_update_list_dict = [history_update.model_dump()]
        else: 
            original_history_dict[current_date] = total
            history_to_update_list_dict = [
                History(day=day, totalValue=Decimal(value)).model_dump()
                for day, value in original_history_dict.items()
            ]
        self._update_item(user_id=user_id,
                          parameter="history",
                          value=history_to_update_list_dict
        )


    def get_user_email_and_history(self, user_id:str) -> tuple:
        user_item = self._get_item(user_id=user_id) 
        print(user_item)
        history_list = user_item.get("history", [])
        return user_item.get("name"), user_item.get("email"), [
            History(day= history["day"], totalValue=history["totalValue"]) for history in history_list
            ]
