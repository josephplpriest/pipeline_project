import pandas as pd

df = pd.read_csv("response.csv", sep="|")

print(df.shape)
df.drop_duplicates(inplace=True)
print(df.shape)