import pandas as pd

def cleaner(df: pd.DataFrame, cols_to_keep: list, remove_metadata: bool=True) -> pd.DataFrame:
    """
    Clean and return dataframe without superfluous columns and metadata

    Takes:
        df - dataframe of posts, one row per post
        cols_to_keep - non-metadata col names as strings, or none to return all
        remove_metadata - defaults to true, removes columns with "." in the name

    Returns:
        df
    """

    #set cols to all if none passed in
    if cols_to_keep == None:
        cols_to_keep = df.columns

    #if we keep the metadata, return all cols we want to keep
    if remove_metadata == True:
        return df[cols_to_keep].copy()
    else:
        return df

