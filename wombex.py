import requests
import pandas as pd
from datetime import datetime
import altair as alt


api_url = 'https://yields.llama.fi/pools'

response = requests.get(api_url)
response_json = response.json()

df = pd.DataFrame(response_json['data'])

wombex = df.loc[(df['chain'] == 'BSC') & (df['exposure'] == 'single') & (df['tvlUsd'] > 5000000)]
print(wombex)
print(wombex[['chain', 'project', 'symbol', 'apyBase', 'apyReward', 'apy']])

wombex = pd.DataFrame({
    'Pool': ['BUSD', 'USDT', 'USDC', 'DAI'],
    'APY': [0.1407, 0.1161, 0.1505, 0.139],
    'TVL': [30990000, 16890000, 9770000, 6100000]
})

print(wombex)

colors = ['#f0df29', '#56d17d', '#1844c7', '#ebbe2a']
dom = ['BUSD', 'USDT', 'USDC', 'DAI']

chart = alt.Chart(wombex).mark_bar(size=30).encode(
    alt.Y('Pool:N', title=None, sort=alt.EncodingSortField(field="TVL", order='descending'), axis=alt.Axis(labelFontWeight=600,)),
    alt.X('APY:Q', title=None, scale=alt.Scale(domain=(0, 0.19)), axis=alt.Axis(format="%")),
)

bars = chart.mark_bar(size=30).encode(
    alt.Color('Pool:N', legend=None, scale=alt.Scale(domain=dom, range=colors))
)

text = chart.mark_text(
    align='left',
    baseline='middle',
    dx=3,  # Nudges text to right so it doesn't appear on top of the bar
    fontWeight=600,
    fontSize=12
).encode(
    text=(alt.Text('APY:Q', format='.2%'))
)

display = (bars + text).properties(
    title="APRs for stablecoins on Wombex",height=180,
).configure_scale(
    bandPaddingOuter=0.2,
    bandPaddingInner=0.1
).configure_axis(
    labelFontSize=11,
    labelPadding=0,
    grid=False,
).configure_title(
    fontSize=14,
    dy=-5 # gives some padding
)

display.save('display.html')