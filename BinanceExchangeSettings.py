import requests
import json

class BinanceTokenSettings:
    def __init__(self, symbol):
        self.symbol = symbol
        # Initializing all properties with default or placeholder values
        self.asset_tick_step = 0  
        self.leverage_mode = 1
        self.leverage_tick_step = 2
        self.limit_fee_pct = 0.0003
        self.market_fee_pct = 0.0006
        self.max_asset_size = 100.0
        self.max_leverage = 150.0
        self.min_asset_size = 0.001
        self.min_leverage = 1.0
        self.mmr_pct = 0.004
        self.position_mode = 3
        self.price_tick_step = 0
        
        self.update_settings_from_binance()

    def update_settings_from_binance(self):
        url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
         
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            symbol_info = next((item for item in data['symbols'] if item['symbol'] == self.symbol), None)
            if symbol_info:
                self.set_properties(symbol_info)                
                
            else:
                print(f"Symbol {self.symbol} not found in exchange information.")
        except requests.RequestException as e:
            print(f"An error occurred while fetching symbol info: {e}")
    def set_properties(self, symbol_info):
        
        filters = {f['filterType']: f for f in symbol_info['filters']}
        price_filter = filters.get('PRICE_FILTER', {})
        lot_size_filter = filters.get('LOT_SIZE', {})
        min_notional_filter = filters.get('MIN_NOTIONAL', {})
        
        # Set properties based on the symbol's info
        self.asset_tick_step = symbol_info.get('pricePrecision', "0")        
        self.max_asset_size = float(price_filter.get('maxPrice', '0'))
        self.min_asset_size = float(price_filter.get('minPrice', '0'))
         
        #     asset_tick_step=6,
        #     leverage_mode=1,
        #     leverage_tick_step=2,
        #     limit_fee_pct=0.0003,
        #     market_fee_pct=0.0006,
        #     max_asset_size=100.0,
        #     max_leverage=50.0,
        
        #     min_asset_size=0.001,
        #     min_leverage=1.0,
        
        #     mmr_pct=0.004,
        #     position_mode=3,
        #     price_tick_step=1,    


    def __repr__(self):
        # Creating a dictionary of all the properties to output
        properties_dict = {
            'symbol': self.symbol,
            'asset_tick_step': self.asset_tick_step,
            'leverage_mode': self.leverage_mode,
            'leverage_tick_step': self.leverage_tick_step,
            'limit_fee_pct': self.limit_fee_pct,
            'market_fee_pct': self.market_fee_pct,
            'max_asset_size': self.max_asset_size,
            'max_leverage': self.max_leverage,
            'min_asset_size': self.min_asset_size,
            'min_leverage': self.min_leverage,
            'mmr_pct': self.mmr_pct,
            'position_mode': self.position_mode,
            'price_tick_step': self.price_tick_step,
        }

        # Converting the dictionary to a JSON string         
        properties_json = json.dumps(properties_dict, indent=4)
        
        return f"{self.__class__.__name__}({properties_json})"