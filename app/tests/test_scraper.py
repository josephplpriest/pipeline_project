import sys
import pytest
sys.path.append('../app')

from src import scraper

headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0"}
url = f"http://www.reddit.com/new.json?limit=25"
response = scraper.get_response(url, headers)

def test_output():
    assert(isinstance(response, dict))


