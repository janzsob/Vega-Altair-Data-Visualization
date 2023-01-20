import requests
import pandas as pd
from datetime import datetime
import altair as alt

# Visualizing transaction history
df = pd.read_csv('avax_transfers.csv').sort_values(by='BLOCK_TIMESTAMP')
print(df.columns)
df = df[['BLOCK_TIMESTAMP', 'ORIGIN_FROM_ADDRESS', 'ORIGIN_TO_ADDRESS', 'AMOUNT', 'AMOUNT_USD']]

df['BLOCK_TIMESTAMP'] = pd.to_datetime(df['BLOCK_TIMESTAMP']).dt.strftime("%Y-%m-%d")
df = df[1:]
df['avax_price'] = df['AMOUNT_USD'] / df['AMOUNT']

print(df)

chart = alt.Chart(df).mark_point().encode(
    alt.X('BLOCK_TIMESTAMP:O'),
    alt.Y('avax_price:Q'),
    alt.Size('AMOUNT:Q')
).properties(width=500)

chart.save('display.html')