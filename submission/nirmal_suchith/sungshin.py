# Sungshin Women's University
# South Korea
# it just has PPT of faculty, so directly creating a list of faculty in os, distributed systems from ppt

professors = []

professors.append({
    "University name": "Sungshin Women's University",
    "country": "South Korea",
    "name": "Shim, Kwang Seob",
    "email": "shim@sungshin.ac.kr",
    "website": None
})

professors.append({
    "University name": "Sungshin Women's University",
    "country": "South Korea",
    "name": "Park, Ji Woong",
    "email": "wpark12@sungshin.ac.kr",
    "website": None
})

professors.append({
    "University name": "Sungshin Women's University",
    "country": "South Korea",
    "name": "Kim, Gyu Yeong",
    "email": "gykim@sungshin.ac.kr",
    "website": None
})

import pandas as pd

df = pd.DataFrame(professors)
df.to_csv("sungshin.csv", index=False)
print("Data saved to sungshin.csv")
