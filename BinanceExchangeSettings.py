import requests

class BinanceExchangeSettings:
    def __init__(self, asset_tick_step, leverage_mode, leverage_tick_step, limit_fee_pct,
                 market_fee_pct, max_asset_size, max_leverage, min_asset_size,
                 min_leverage, mmr_pct, position_mode, price_tick_step):
        self.asset_tick_step = asset_tick_step
        self.leverage_mode = leverage_mode
        self.leverage_tick_step = leverage_tick_step
        self.limit_fee_pct = limit_fee_pct
        self.market_fee_pct = market_fee_pct
        self.max_asset_size = max_asset_size
        self.max_leverage = max_leverage
        self.min_asset_size = min_asset_size
        self.min_leverage = min_leverage
        self.mmr_pct = mmr_pct
        self.position_mode = position_mode
        self.price_tick_step = price_tick_step

    def update_exchange_settings(self, api_response):
        self.price_tick_step = int(api_response['pricePrecision'])
        self.asset_tick_step = int(api_response['quantityPrecision'])
        # Add more mappings as per your requirements.

    def fetch_and_update_settings(self, symbol):
        url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises stored HTTPError, if one occurred.
            
            symbols_info = response.json()['symbols']
            for info in symbols_info:
                if info['symbol'] == symbol:
                    self.update_exchange_settings(info)
                    print(f"Settings updated for {symbol}")
                    break
            else:
                print(f"Symbol {symbol} not found in exchange info.")
        except requests.RequestException as e:
            print(f"An error occurred: {e}")