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

#looked for qs that had 90% similar text 
# manually inspected which ones were essentailly copies to choose which to drop
drop_list = [
    5, 7, 8, 9, 38, 48, 81, 82, 106, 162, 385, 386, 535, 683, 1664, 1568, 1574, 
    1578, 1582, 1583, 1587, 1589, 1590, 1595, 1596, 1599, 1602, 1606, 1607, 1616, 1623
]

df = df.drop(drop_list, axis="index").reset_index(drop=True)

df.to_csv("./data/clean_ballot_qs.csv")

