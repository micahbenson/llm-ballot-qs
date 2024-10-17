import pandas as pd
import numpy as np

#Read in data
df = pd.read_csv("./data/ballot_qs.csv")

#Drop rows 
#There are duplicate ballot qs with the same summary but different categories so drop these
df = df.drop_duplicates(subset='Summary')
df = df.dropna(subset="Percent_Yes")
df = df.dropna(subset="Summary")
df = df.drop(df[df["Percent_Yes"]=="Percent Yes"].index)
df = df.drop(columns="Status")

#Convert percent strings to floats
df["Percent_Yes"] = df['Percent_Yes'].apply(lambda x: float(x.rstrip("%")) / 100)

#One hot encode whether the question passed
df["Pass"] = df["Percent_Yes"].apply(lambda x: 1 if x > 0.5 else 0)

df = df.reset_index(drop=True)

df.to_csv("./data/clean_ballot_qs.csv")

