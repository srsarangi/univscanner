# Sungshin Women's University
# South Korea
# it just has PPT of faculty, so directly creating a list of faculty in os, distributed systems from ppt

def sungshin():

    professors = []

    university_name = "Sunghin Women's University"
    country = "South Korea"

    # professors.append({
    #     "University name": "Sungshin Women's University",
    #     "country": "South Korea",
    #     "name": "Shim, Kwang Seob",
    #     "email": "shim@sungshin.ac.kr",
    #     "website": None
    # })

    professors.append([university_name, country, "Shim, Kwang Seob", "shim@sungshin.ac.kr", None])

    # professors.append({
    #     "University name": "Sungshin Women's University",
    #     "country": "South Korea",
    #     "name": "Park, Ji Woong",
    #     "email": "wpark12@sungshin.ac.kr",
    #     "website": None
    # })
    professors.append([university_name, country, "Park, Ji Woong", "wpark12@sungshin.ac.kr", None])

    # professors.append({
    #     "University name": "Sungshin Women's University",
    #     "country": "South Korea",
    #     "name": "Kim, Gyu Yeong",
    #     "email": "gykim@sungshin.ac.kr",
    #     "website": None
    # })

    professors.append([university_name, country, "Kim, Gyu Yeong", "gykim@sungshin.ac.kr", None])



    # import pandas as pd

    # df = pd.DataFrame(professors)
    # df.to_csv("sungshin.csv", index=False)
    # print("Data saved to sungshin.csv")

    print("Sungshin data extracted successfully")
    return professors
