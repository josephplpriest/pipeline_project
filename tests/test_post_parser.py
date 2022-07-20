import json
import os
import sys
import pytest
import pandas as pd


sys.path.append('../app')

from src import post_parser

# Use previously downloaded text data for mock input

with open("tests/response.txt") as f:
    text = f.read()
    mock_object = json.loads(text)

def test_invalid_input1():
    with pytest.raises(ValueError):
        post_parser.parser("some_string")

def test_invalid_input2():
    with pytest.raises(ValueError):
        post_parser.parser({})

def test_invalid_input3():
    with pytest.raises(ValueError):
        post_parser.parser([1,3,5])

def test_valid_input():
    #mock returned value
    returned_val = post_parser.parser(mock_object)
    
    #type checking
    assert(type(returned_val)==pd.DataFrame)

    #check that number of rows is equal to reddit default, columns can vary based on metadata returned
    assert(returned_val.shape[0] == 25)

