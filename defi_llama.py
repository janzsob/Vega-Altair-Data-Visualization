import requests
import pandas as pd
from datetime import datetime
import altair as alt

api_url = "https://yields.llama.fi/pools"

response = requests.get(api_url)
response_json = response.json()

df = pd.DataFrame.from_dict(response_json['data'])

op = df.loc[df['chain'] == 'Optimism']

beethoven = op.loc[op['project'] == 'beethoven-x']
#print(beethoven.loc[beethoven["symbol"] == 'WETH-RETH'])

rocket_pool = beethoven.loc[beethoven["symbol"] == 'WETH-RETH']

#print(rocket_pool)

pool_chart_url = 'https://yields.llama.fi/chart/74c48bf7-54fc-4110-a429-364b3c73ba3b'
r = requests.get(pool_chart_url)
r_json = r.json()
#print(r_json)

rocket_df = pd.DataFrame.from_dict(r_json['data'])
#print(rocket_df)

historical_rocket_pool = pd.DataFrame({
    'Date': pd.to_datetime(rocket_df["timestamp"]).dt.strftime("%Y-%m-%d"),
    'TVL': rocket_df['tvlUsd'],
    'APY': rocket_df['apy']

})

print(historical_rocket_pool)

chart1 = alt.Chart(historical_rocket_pool).mark_line(interpolate='monotone').encode(
    alt.X('Date:T'),
    alt.Y('APY:Q'),
    tooltip = [
        alt.Tooltip('Date:T'),
        alt.Tooltip('APY:Q')
    ]
).properties(width=600, title="ETH Rocket pool on Beethoven X")

chart2 = alt.Chart(historical_rocket_pool).mark_line(interpolate='monotone', stroke='orange').encode(
    alt.X('Date:T'),
    alt.Y('TVL:Q'),
    tooltip = [
        alt.Tooltip('Date:T'),
        alt.Tooltip('TVL:Q')
    ]
).properties(width=600)

display = alt.layer(chart1, chart2).resolve_scale(y='independent')

display.save('display.html')