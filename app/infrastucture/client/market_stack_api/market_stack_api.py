import httpx

from app.domain.ports.stock_api_port import StockApiPort
from app.settings import Settings
from app.infrastucture.client.market_stack_api.serializers import StockDetails 

settings = Settings()

class MarketStackApi(StockApiPort):
    async def _fetch_price_data(self, index: str) -> StockDetails:
        async with httpx.AsyncClient() as client:
            url = settings.market_stack_settings.build_price_eod_url(symbol=index)
            print("URL to call is: ", url)
            response: httpx.Response = await client.get(url)
            response.raise_for_status()
            return StockDetails.model_validate_json(response.text)
            ''' response_json = """
            {
            "pagination": {
                "limit": 100,
                "offset": 0,
                "count": 100,
                "total": 100
            },
            "data": [
                {
                "open": 0,
                "high": 0,
                "low": 0,
                "close": 911.5,
                "volume": 100,
                "adj_high": null,
                "adj_low": null,
                "adj_close": 97.5,
                "adj_open": null,
                "adj_volume": null,
                "split_factor": 1,
                "dividend": 0,
                "symbol": "BGO.L",
                "exchange": "XLON",
                "date": "2025-10-20T00:00:00+0000"
                },
                {
                "open": 98.75,
                "high": 100,
                "low": 95,
                "close": 9111.5,
                "volume": 78576,
                "adj_high": null,
                "adj_low": null,
                "adj_close": 97.5,
                "adj_open": null,
                "adj_volume": null,
                "split_factor": 1,
                "dividend": 0,
                "symbol": "BGO.L",
                "exchange": "XLON",
                "date": "2025-10-17T00:00:00+0000"
                },
                {
                "open": 91.561,
                "high": 95,
                "low": 90,
                "close": 94,
                "volume": 22853,
                "adj_high": null,
                "adj_low": null,
                "adj_close": 94,
                "adj_open": null,
                "adj_volume": null,
                "split_factor": 1,
                "dividend": 0,
                "symbol": "BGO.L",
                "exchange": "XLON",
                "date": "2025-10-10T00:00:00+0000"
                },
                {
                "open": 96.555,
                "high": 121.75,
                "low": 95,
                "close": 117.5,
                "volume": 252424,
                "adj_high": null,
                "adj_low": null,
                "adj_close": 117.5,
                "adj_open": null,
                "adj_volume": null,
                "split_factor": 1,
                "dividend": 0,
                "symbol": "BGO.L",
                "exchange": "XLON",
                "date": "2025-10-12T00:00:00+0000"
                }
            ]
            }
            """
            # return  StockDetails.model_validate_json(response_json)
            '''
        

    async def get_price_eof(self, index: str) -> float:
        stock_response = await self._fetch_price_data(index)
        stock_response_data = stock_response.data
        filtered = [x for x in stock_response_data if x.open != 0]
        filtered.sort(key=lambda x: x.date, reverse=True)
        return filtered[0].close
     
    
 
