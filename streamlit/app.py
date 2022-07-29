import streamlit as st
import pandas as pd
import plotly.express as px
import time



try:
    df = pd.read_csv("data/response.csv", header=0, delimiter="|", engine='python', on_bad_lines="skip")
except FileNotFoundError:
    time.sleep(5)
    df = pd.read_csv("data/response.csv", header=0, delimiter="|", engine='python', on_bad_lines="skip")

# most recently scraped time, number of posts
most_recent_post = max(df.created)[:-6]

st.write(f"Last post scraped at {most_recent_post}")

df = df.drop_duplicates(subset=["title", "author"])

st.write(df)

fig = px.bar(df.subreddit.value_counts().head(10))
st.plotly_chart(fig)

fig = px.bar(df.author.value_counts().head(10))
st.plotly_chart(fig)
