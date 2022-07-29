import sqlite3
import pprint
import pandas as pd

conn = sqlite3.connect("data/scraping_stats.db")

cur = conn.cursor()


pp = pprint.PrettyPrinter(indent=4)

def sql_cmd(cmd_string):
    """Helper function to return sql query as a string"""
    result = cur.execute(cmd_string)
    return result

def query_pp(response):
    """Pretty print the response with the column names"""
    columns = [x[0] for x in [*data.description]]
    res = data.fetchall()
        
    df = pd.DataFrame(data = res, columns = columns)
    print(df)

data = sql_cmd("SELECT * FROM logging_stats")

print("\nSELECT * FROM logging_stats")

query_pp(data)

conn.close()