import requests
from utils.logger import get_logger

logger = get_logger()

def fetch_api_data(url, method="GET", params=None, retries=3, timeout=30):
    for attempt in range(retries):
        try:
            resp = requests.request(method, url, params=params, timeout=timeout)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logger.error(f"API fetch failed (attempt {attempt+1}/{retries}): {e}")
            if attempt == retries - 1:
                raise