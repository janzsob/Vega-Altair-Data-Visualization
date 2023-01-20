import requests
import pandas as pd
from datetime import datetime
import altair as alt


protocol = 'beethoven-x'
api_url = f"https://api.llama.fi/protocol/{protocol}"

response = requests.get(api_url)
response_json = response.json()

op_tvl = pd.DataFrame.from_dict(response_json['chainTvls']['Optimism']['tvl'])
ftm_tvl = pd.DataFrame.from_dict(response_json['chainTvls']['Fantom']['tvl'])

# Forming dates
op_tvl['date'] = pd.to_datetime(op_tvl['date'], unit='s').dt.strftime("%Y-%m-%d")
ftm_tvl['date'] = pd.to_datetime(ftm_tvl['date'], unit='s').dt.strftime("%Y-%m-%d")
# Forming floats
pd.options.display.float_format = '${:,.0f}'.format

# Filter period in FTM
ftm_tvl = ftm_tvl.loc[ftm_tvl['date'] > '2022-06-08',]
#ftm_tvl.reset_index(drop=True, inplace=True) # Reset index from 0

# Add category column
op_tvl['category'] = 'Optimism'
ftm_tvl['category'] = 'Fantom'

#print(ftm_tvl)

# merge dataframes
merged_tvl = pd.concat([op_tvl, ftm_tvl], ignore_index=True)
merged_tvl.rename(columns={'totalLiquidityUSD': 'tvl'}, inplace=True)
print(merged_tvl)

# Delete data duplication
merged_tvl = merged_tvl.loc[merged_tvl['date'] < '2022-11-16']
#print(merged_tvl)

# Chart
colors = ['#1176f2', '#ed4940']

chart = alt.Chart(merged_tvl).mark_area(interpolate='monotone').encode(
    alt.Y('tvl:Q', title=None, axis=alt.Axis(offset=5, format='$,.0r'), scale=alt.Scale(domain=[0, 100000000])),
    alt.X('date:T', title=None, axis=alt.Axis(offset=5)),
    alt.Color('category:N', legend=alt.Legend(title="Chains"), scale=alt.Scale(range=colors)),
    tooltip = [
        alt.Tooltip('category:N'),
        alt.Tooltip('tvl:Q'),
        alt.Tooltip('date:T')
    ]
).properties(title='Beethoven X TVL', width=500).configure_axis(labelFontSize=12).configure_legend(titleFontSize=13,
labelFontSize=12).configure_title(fontSize=14)

chart.save('display.html')