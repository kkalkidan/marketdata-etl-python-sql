import pandas as pd
import requests

from utils.config import get_value
from utils.parser import write_json, load_json


ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"
DAILY_DATA_KEY = "Time Series (Daily)"
METADATA_KEY = "Meta Data"
DIVIDENDS_KEY = "data"

def load_alpha_vantage_data(function: str, symbol: str, apikey: str)-> dict:
    """Load OHLCV data from Alpha Vantage API."""
    try:
        response = requests.get(
            ALPHA_VANTAGE_URL,
            params={
                "function": function,
                "symbol": symbol,
                "apikey": apikey,
            },
            timeout=10,
        )
        if response.status_code != 200:
            raise ValueError(
                f"Failed to load OHLCV data: {response.status_code} "
                f"{response.text}"
            )

        return response.json()
    except Exception as e:
        raise Exception(f"Something went wrong: {e}")


def column_name(name: str) -> str:
    """Turn fieldname into snake_case name."""
    return name.split(". ")[1].lower().replace(" ", "_")


def parse_ohlcv_daily_data(data: dict) -> pd.DataFrame:
    """Parse OHLCV daily data into a pandas DataFrame."""
    prices = pd.DataFrame.from_dict(data[DAILY_DATA_KEY], orient="index")
    prices.index = pd.to_datetime(prices.index)
    prices.index.name = "date"
    prices = prices.rename(columns=column_name)
    prices = (
            prices.apply(pd.to_numeric)
            .sort_index()
            .reset_index()
        )

    metadata = pd.DataFrame.from_dict(data[METADATA_KEY], orient="index").T
    metadata = metadata.rename(columns=column_name)
    return prices.merge(metadata, how="cross")

def parse_corporate_actions(data: dict) -> pd.DataFrame:
    """Parse corporate actions data."""
    dividends = pd.DataFrame(data[DIVIDENDS_KEY])
    return dividends



if __name__ == "__main__":
    """For testing purposes."""
    alphavantage_api_key = get_value("ALPHAVANTAGE_API_KEY")
    ohlcvdata = load_json("data/sample_ohlcv_daily.json")
    dividends = load_json("data/sample_dividends.json")
    if not ohlcvdata:
        ohlcvdata = load_alpha_vantage_data("TIME_SERIES_DAILY", "IBM", alphavantage_api_key)
        write_json(ohlcvdata, "data/sample_ohlcv_daily.json")
    if not dividends:
        dividends = load_alpha_vantage_data("IBM", "DIVIDENDS", alphavantage_api_key)
        write_json(dividends, "data/sample_dividends.json")
    print(parse_corporate_actions(dividends))
    # print(parse_ohlcv_daily_data(ohlcvdata))
