import requests
import pandas as pd
from datetime import datetime
import altair as alt

api_url = "https://yields.llama.fi/pools"

response = requests.get(api_url)
response_json = response.json()

df = pd.DataFrame.from_dict(response_json['data'])
#print(df.columns)
#print(df.head())

eth_pools = df[["chain", "project", "symbol", "tvlUsd", 'apy', 'apyBase', 'apyReward']]

eth_pools = eth_pools.loc[
    ((df['chain'] == "Arbitrum") | (df['chain'] == "Optimism")) & 
    (df['apy'] > 5) & 
    (df['tvlUsd'] > 500000) &
    (df['symbol'].str.startswith(('ETH','WETH', 'SETH', 'WSTETH', 'ALETH'))) &
    (df['symbol'].str.endswith(('ETH', 'WETH', 'SETH', 'RETH')))
] 

pd.options.display.float_format = '{:.2f}'.format


#eth_pools['name'] = eth_pools.project.str.cat(eth_pools.symbol, sep=': ')

#eth_pools["tvlUsd"] = eth_pools['tvlUsd'].apply('${:,}'.format)

print(eth_pools)

# Save data in an excel file
writer = pd.ExcelWriter('pool_table.xlsx')
eth_pools.to_excel(writer)
writer.save()

range_ = ['blue', 'red']

chart = alt.Chart(eth_pools).mark_point().encode(
    alt.X('tvlUsd:Q'),
    alt.Y('apy:Q'),
    alt.Color('chain:N', scale=alt.Scale(range=range_)),
    alt.Shape('name:N')
)

text = chart.mark_text(
    align='left',
    baseline='middle',
    dx=7
).encode(
    text='name'
)

display = chart + text

display.save('display.html')