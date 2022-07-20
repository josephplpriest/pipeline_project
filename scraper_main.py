import time
import datetime as dt

import sqlite3
from sqlite3 import Error

import pandas as pd
from src import scraper, post_parser, clean_df

POST_REQUEST_NUMBER = 100


def main():

    conn = sqlite3.connect("scraping_stats.db")

    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0"}
    url = f"http://www.reddit.com/new.json?limit={POST_REQUEST_NUMBER}"
   
    for _ in range(5):
        # get json response as python dict
        post_json = scraper.get_response(url, headers)

        if post_json == None:
            print("No response", dt.datetime.now().strftime('%Y-%m-%D %H:%M:%S'))

        df = post_parser.parser(post_json)

        cols_to_keep = [
                        "subreddit", 
                        "selftext", 
                        "title", 
                        "subreddit_name_prefixed", 
                        "link_flair_text", 
                        "link_flair_type", 
                        "is_self", 
                        "over_18", 
                        "permalink", 
                        "url", 
                        "subreddit_subscribers",
                        ]

        cleaned_df = clean_df.cleaner(df, cols_to_keep=cols_to_keep)

        cleaned_df.to_csv("response.csv", index=False, header=True, sep="|", mode="a")


        #Track metrics for each iterations
        output = []

        #logging time
        output.append(("logging_time", dt.datetime.now().strftime('%D %H:%M:%S')))

        #text columns to check for nans
        subset_df = cleaned_df[["selftext", "link_flair_text", "title"]]

        for col in subset_df.isna().sum().reset_index().values.tolist():
            output.append((col[0]+"_prop_na", col[1]/cleaned_df.shape[0]))

        #check adult for content
        output.append(("over_18_posts_prop", sum(cleaned_df["over_18"]/len(cleaned_df.over_18))))

        #most popular sub
        
        subreddit = cleaned_df["subreddit"][cleaned_df["subreddit_subscribers"] == cleaned_df["subreddit_subscribers"].max()].values[0]
        count = cleaned_df["subreddit_subscribers"].max()

        output.append(("most_popular_sub", subreddit))
        output.append(("count_most_pop_sub", count))

        #average length of raw text posts
        post_mean_len = cleaned_df[cleaned_df["selftext"].notnull()]["selftext"].apply(lambda x: len(x.split())).mean()

        output.append(("mean_selftext_len", post_mean_len))

        out_dict = {k:[v] for k,v in output}

        stats = pd.DataFrame(out_dict)
        print(stats.head(1), flush=True)
        

        stats.to_sql(con=conn, name="logging_stats", if_exists="append")
        
        
        time.sleep(2)


    conn.close()

if __name__ == "__main__":
    main()