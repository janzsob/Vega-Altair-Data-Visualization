import requests
import pandas as pd
from datetime import datetime
import altair as alt
from not_public import ADDRESS, APIKEY

page = 1
offset = 200
api_url = f'https://api.bscscan.com/api?module=account&action=txlist&address={ADDRESS}&startblock=0&endblock=99999999&page={page}&offset={offset}&sort=asc&apikey={APIKEY}'

response = requests.get(api_url)

response_json = response.json()

""" Number of transactions on a certain BSC address """

df = pd.DataFrame.from_dict(response_json['result'])

print("")
print(df.loc[100])

# # Number of transactions with dates
# transactions = pd.DataFrame({
#     "timeStamp": pd.to_datetime(df['timeStamp'], unit='s').dt.strftime("%Y-%m-%d")
# })

#print(transactions)
#print("")

# chart = alt.Chart(transactions).mark_line(point=True).encode(
#     alt.X('timeStamp:O'),
#     alt.Y('count()'),
#     tooltip = [
#         alt.Tooltip('count()'),
#         alt.Tooltip('timeStamp:O')
#     ]
# )

df_gas = pd.DataFrame({
    "timeStamp": pd.to_datetime(df['timeStamp'], unit='s').dt.strftime("%Y-%m-%d"),
    "gas": df["gas"]
})

print(df_gas)

chart = alt.Chart(df_gas).mark_area(interpolate='monotone').encode(
    alt.X("timeStamp:O"),
    alt.Y("gas:Q"),
    tooltip = [
        alt.Tooltip('gas:Q'),
        alt.Tooltip('timeStamp:O')
    ]
)

chart.save('display.html')
