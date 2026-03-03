from pydantic_settings import BaseSettings, SettingsConfigDict


class MarketStackSettings(BaseSettings):
    base_url: str | None = "http://localhost:8081"
    price_eod_endpoint: str | None = "/v2/eod?access_key={access_key}&symbols={symbol}"
    api_key: str | None = "f3715ce587da03a5cfda92f9fa6a40a9"
    model_config = SettingsConfigDict(env_prefix='EXTERNAL_PRICE_API_PROVIDER_')
    def build_price_eod_url(self, symbol: str):
        endpoint = self.price_eod_endpoint.format(access_key = self.api_key, symbol=symbol)
        return f"{self.base_url}{endpoint}"
    

class Settings(BaseSettings):
    auth_user: str | None = None
    auth_pass: str | None = None
    
    market_stack_settings : MarketStackSettings = MarketStackSettings()

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

