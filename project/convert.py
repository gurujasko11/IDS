import pandas as pd
import json
import requests
import math
import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib import cm
from pandas import Series

house_df = pd.read_csv('kc_house_data.csv')
elevation_results = []
query_size = 1000
j = 0
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
number_of_requests = math.ceil(len(house_df)/query_size)
while j*query_size < len(house_df):
    data = {
        "locations": []
    }
    data_end = min((j+1)*query_size,len(house_df))
    for i in range(j*query_size, data_end):
        item = {}
        item["latitude"] = house_df["lat"][i]
        item["longitude"] = house_df["long"][i]
        data["locations"].append(item)
    print("Sending request "+str(j+1)+" of "+str(number_of_requests))
    r = requests.post("https://api.open-elevation.com/api/v1/lookup", data=json.dumps(data), headers=headers)
    resp = json.loads(r.content)
    for item in resp["results"]:
        elevation_results.append(item["elevation"])
    j += 1

house_df['ele'] = Series(elevation_results, index=house_df.index)

house_df.to_csv("output.csv", sep=',')
print("koniec")
