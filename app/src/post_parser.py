import json
import pandas as pd

def parser(post_text: dict) -> pd.DataFrame:
    """
    Gets post details, organized by row
    
    Args:
        post_text: full response object as json

    Returns:
        Combined dataframe of all posts
    """
    if isinstance(post_text, dict) != True:
        raise ValueError

    #parsing json nesting
    _, post_data = post_text.items()
    _, post_dict = post_data

    #where we'll store each post before concatenating them
    df_list = []

    #convert json data to df and append
    for post in post_dict["children"]:
        post_details = post['data']
        df = pd.json_normalize(post_details)
        df_list.append(df)

    combined_df = pd.concat(df_list, ignore_index=True)

    return combined_df