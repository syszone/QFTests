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
        self.max_leverage = 50.0
        self.min_asset_size = 0.001
        self.min_leverage = 1.0
        self.mmr_pct = 0.004
        self.position_mode = 3
        self.price_tick_step = 0
        
        self.update_settings_from_binance()

    def update_settings_from_binance(self):
        url = "https://api.binance.com/api/v3/exchangeInfo"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            symbol_info = next((item for item in data['symbols'] if item['symbol'] == self.symbol), None)
            if symbol_info:
                
                filters = {f['filterType']: f for f in symbol_info['filters']}
                price_filter = filters.get('PRICE_FILTER', {})
                lot_size_filter = filters.get('LOT_SIZE', {})
                min_notional_filter = filters.get('MIN_NOTIONAL', {})
                
                # Mapping Binance response to class properties with adjustments for tick steps
                self.max_leverage = 50.0  # Binance does not provide this directly; may need another API call or default setting
                self.min_leverage = 1.0   # Assuming a default min leverage
                # Storing as formatted strings directly
                self.max_asset_size = "{:.8f}".format(float(lot_size_filter.get('maxQty', '0')))
                self.min_asset_size = "{:.8f}".format(float(lot_size_filter.get('minQty', '0')))
                
                # Calculate the number of decimal places for asset_tick_step and price_tick_step
                self.asset_tick_step = len(lot_size_filter.get('stepSize', '1').split('.')[-1]) if '.' in lot_size_filter.get('stepSize', '1') else 0
                self.price_tick_step = len(price_filter.get('tickSize', '1').split('.')[-1]) if '.' in price_filter.get('tickSize', '1') else 0
                
                self.leverage_tick_step = 0.01  # Binance does not directly provide this; you might need to set a default or derive it
                
                # Additional properties like min_notional can also be set here
                self.min_notional = float(min_notional_filter.get('notional', '0'))
                
            else:
                print(f"Symbol {self.symbol} not found in exchange information.")
        except requests.RequestException as e:
            print(f"An error occurred while fetching symbol info: {e}")
 
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