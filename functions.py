"""
This module contains all the functions that are available to the chatGPT assistant.
"""

import json
import requests

# keep track of every function
functions = []
available_functions = {}

def get_crypto_info(symbol):
    """Get the current information for a given cryptocurrency"""
    symbol = symbol.lower()

    crypto_info = requests.get(f"https://api.coingecko.com/api/v3/coins/{symbol}").json()
    
    crypto_data = {
        "name": crypto_info["name"],
        "sentiment_votes_up_percentage": crypto_info["sentiment_votes_up_percentage"],
        "sentiment_votes_down_percentage": crypto_info["sentiment_votes_down_percentage"],
        "market_cap_rank": crypto_info["market_cap_rank"],
        "price": crypto_info["market_data"]["current_price"]["usd"],
    }

    return json.dumps(crypto_data)

# add function to list of functions
functions.append( {
            "name": "get_crypto_info",
            "description": "Get the current information for a given cryptocurrency",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "The symbol of the cryptocurrency, e.g. bitcoin",
                    }
                },
                "required": ["symbol"]
            }
        }
    )

# add function to available functions
available_functions["get_crypto_info"] = get_crypto_info