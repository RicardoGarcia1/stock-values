from pydantic_settings import BaseSettings


class MarketStackSettings(BaseSettings):
    base_url: str | None = "http://api.marketstack.com"
    price_eod_endpoint: str | None = "/v2/eod?access_key={access_key}&symbols={symbol}"
    api_key: str | None = "f3715ce587da03a5cfda92f9fa6a40a9"
    class Config:
        env_prefix = "EXTERNAL_PRICE_API_PROVIDER_"  

    def build_price_eod_url(self, symbol: str):
        endpoint = self.price_eod_endpoint.format(access_key = self.api_key, symbol=symbol)
        return f"{self.base_url}{endpoint}"
    

class Settings(BaseSettings):
    auth_user: str | None = None
    auth_pass: str | None = None
    
    market_stack_settings : MarketStackSettings = MarketStackSettings()

    class Config:
        env_file = ".env"

