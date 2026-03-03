import json
from pathlib import Path
from typing import List

from pydantic import BaseModel
from app.domain.models.user_data import History, Stock, User
from app.domain.ports.user_data_repository_port import UserDataRepositoryPort
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[3] 
DATA_PATH = BASE_DIR / "data" / "users.json"

class UsersInfo(BaseModel):
    users_info: List[User]
    
class JSONUserDataRepository(UserDataRepositoryPort):
    def _get_user_info_from_json(self): 
        if not DATA_PATH.exists(): 
            raise FileNotFoundError("Data file not found")
        with DATA_PATH.open("r", encoding= "utf-8") as f:
            data = json.load(f)
        return UsersInfo(users_info=data)
   
    
    def _update_user_info(self, users_info):
        with DATA_PATH.open("w", encoding="utf-8") as f:
            json.dump(users_info.model_dump()["users_info"], f, indent=4, ensure_ascii=False)


    def add_user(self, new_user: User):
        users_info = self._get_user_info_from_json()
        for user in users_info.users_info:
             if new_user.user_identifier == user.user_identifier:
                 raise ValueError("User already exists")
        users_info.users_info.append(new_user)
        self._update_user_info(users_info=users_info)
        return 
   

    def delete_user(self, user_id:str):
        users_info = self._get_user_info_from_json()
        users_info.users_info = [user for user in users_info.users_info if user.user_identifier != user_id ]
        self._update_user_info(users_info=users_info)
        return 
    

    def patch_user(self, user_to_update: User):
        users_info = self._get_user_info_from_json()
        for user_info in users_info.users_info:
            # Checking the user tu update
            user_found = False
            if user_info.user_identifier == user_to_update.user_identifier:
                user_found = True
                # Original stock list 
                original_stock_dict = {x.index : x for x in user_info.stocks}
                # New stock list to update
                for stock in user_to_update.stocks:
                    if stock.index in original_stock_dict:
                        original_stock_dict[stock.index] = original_stock_dict[stock.index].model_copy(
                            update=stock.model_dump(exclude_unset=True)
                            )
                    else:
                      original_stock_dict[stock.index] = stock
                user_info.stocks = [ Stock.model_validate(x) for x in original_stock_dict.values()]
                break
            # Updating stock or returning error
        if user_found:
            self._update_user_info(users_info=users_info)   
            return True   
        else:
            return False


    def get_stocks_by_user(self, user_id: str) -> Stock:
        users_info = self._get_user_info_from_json()
        for user_info in users_info.users_info:
            if user_info.user_identifier == user_id:
                return user_info.stocks
        return []


    def add_or_update_history_record(self, total:float, user_id:str):
        users_info = self._get_user_info_from_json()
        for user_info in users_info.users_info:
            if user_info.user_identifier == user_id:
                today_str = datetime.now().strftime("%d/%m/%Y")
                if user_info.history is not None:
                    existing = next((h for h in user_info.history if h.day == today_str), None)
                    if existing:
                        existing.totalValue = total
                        print(f"Update info to {user_id} history: {existing}")
                    else:
                        new_history = History(day=today_str, totalValue=total)
                        user_info.history.append(History(day=today_str, totalValue=total))
                        print(f"Adding info to {user_id} history: {new_history}")
                else: 
                    new_history_list: List[History] = [History(day=today_str, totalValue=total)]
                    user_info.history = new_history_list
                    print(f"Adding info to {user_id} history: {new_history_list[0]}")
        self._update_user_info(users_info= users_info)
        return 