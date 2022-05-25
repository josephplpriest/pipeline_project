import sys

import pandas as pd
import pytest

sys.path.append('../pipeline_project')

from src import clean_df
@pytest.fixture(name="df")
def mock_object():
    return pd.DataFrame({"names": ["paul", "duane", ""],
                        "grades": ["", "", 85], 
                        "meta.data": ["","",""],
                        })

@pytest.fixture(name="cols")
def cols():
    return ["names"]

def test_valid_input(df, cols):
    assert(isinstance(clean_df.cleaner(df, cols), pd.DataFrame) == True)

def test_invalid_input():
    with pytest.raises(AttributeError):
        clean_df.cleaner([],[])
