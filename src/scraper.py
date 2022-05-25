import json
import pandas as pd
import requests


def get_response(url: str, headers: dict) -> dict:
    """
    Returns a dict object of the response, or none if status_code is an error

    Args:
        url -> website to return info from
        headers -> headers to pass to avoid scraping blockers

    Returns:
        dict or None
    """

    response = requests.get(url=url, headers=headers)

    if (response.status_code == 200) == False:
        return None
    else:
        return response.json()

