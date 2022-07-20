import datetime as dt
from distutils.command.config import config
import time
import logging

import sqlite3
from sqlite3 import Error

import pandas as pd
from src import scraper, post_parser, clean_df
import yaml

from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

with open("config.yml", mode="r", encoding="utf-8") as file:
    try:
        config = yaml.safe_load(file)
    except yaml.YAMLError as exc:
        print(exc)


logging.basicConfig(filename = config["log_file"], encoding='utf-8', level=logging.DEBUG)


POST_REQUEST_NUMBER = config["n_posts"]


def main():

    conn = sqlite3.connect("scraping_stats.db")

    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0"}
    url = f"http://www.reddit.com/new.json?limit={POST_REQUEST_NUMBER}"

    logging.info("Starting scraper")

    for _ in range(config["n_iterations"]):
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

        cleaned_df["selftext"] = cleaned_df["selftext"].str.replace("\n", " ")

        cleaned_df.to_csv("response.csv", index=False, header=True, sep="|", mode="a")


        #Track metrics for each iterations
        output = []

        #logging time
        output.append(("logging_time", dt.datetime.now().strftime('%D %H:%M:%S')))

        #check adult for content
        output.append(("over_18_posts_prop", sum(cleaned_df["over_18"]/len(cleaned_df.over_18))))

        #most popular sub metrics
        subreddit = cleaned_df["subreddit"][cleaned_df["subreddit_subscribers"] == cleaned_df["subreddit_subscribers"].max()].values[0]
        count = cleaned_df["subreddit_subscribers"].max()

        #add to output
        output.append(("most_popular_sub", subreddit))
        output.append(("count_most_pop_sub", count))

        #average length of raw text posts
        post_mean_len = cleaned_df[cleaned_df["selftext"].notnull()]["selftext"].apply(lambda x: len(x.split())).mean()

        output.append(("mean_selftext_len", post_mean_len))

        output.append(("common_subreddit", cleaned_df["subreddit"].value_counts().index[0]))

        output.append(("count_common_sub", cleaned_df["subreddit"].value_counts()[0]))

        out_dict = {k:[v] for k,v in output}

        stats = pd.DataFrame(out_dict)

        print(stats.head(1), flush=True, end="\n"*2)
        
        logging.debug("Writing to SQLite")

        stats.to_sql(con=conn, name=config["log_table"], if_exists="append")
        
        
        time.sleep(4)


    conn.close()

    logging.info("Scraping Finished")

if __name__ == "__main__":
    main()