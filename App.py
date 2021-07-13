# Import dependencies
import streamlit as st
import pandas as pd
import plotly.express as px
from bs4 import BeautifulSoup
import requests
import json
import time

# App Title
st.title('Crypto App')
#st.subtitle('Dashboard')

# About
st.markdown("""
Carry out analysis on top 100 crypto coins. Live data gotten from [CoinMarketCap](wwww.coinmarketcap.com). Powered by FOR|DATA.
""")

# Web scraping
@st.cache
def load_data():
    cmc = requests.get('https://coinmarketcap.com')
    soup = BeautifulSoup(cmc.content, 'html.parser')

    data = soup.find('script', id='__NEXT_DATA__', type='application/json')
    coins = {}
    coin_data = json.loads(data.contents[0])
    listings = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']
    for i in listings:
      coins[str(i['id'])] = i['slug']

    coin_name = []
    coin_symbol = []
    market_cap = []
    percent_change_1h = []
    percent_change_24h = []
    percent_change_7d = []
    price = []
    volume_24h = []

    #currency_price_unit = ['BTC', 'ETH', 'USD']
    for i in listings:
      coin_name.append(i['slug'])
      coin_symbol.append(i['symbol'])
      price.append(i['quote']['USD']['price'])
      percent_change_1h.append(i['quote']['USD']['percentChange1h']) # percent_change_1h
      percent_change_24h.append(i['quote']['USD']['percentChange24h']) #percent_change_24h
      percent_change_7d.append(i['quote']['USD']['percentChange7d']) # percent_change_7d
      market_cap.append(i['quote']['USD']['marketCap']) # market_cap
      volume_24h.append(i['quote']['USD']['volume24h']) # volume_24h

    df = pd.DataFrame(columns=['coin_name', 'coin_symbol', 'marketCap', 'percentChange1h', 'percentChange24h', 'percentChange7d', 'price', 'volume24h'])
    df['coin_name'] = coin_name
    df['coin_symbol'] = coin_symbol
    df['price'] = price
    df['percentChange1h'] = percent_change_1h
    df['percentChange24h'] = percent_change_24h
    df['percentChange7d'] = percent_change_7d
    df['marketCap'] = market_cap
    df['volume24h'] = volume_24h
    return df
df = load_data()
numeric_df = df.select_dtypes(['float', 'int'])
numeric_cols = numeric_df.columns
unique_coins = df['coin_symbol'].unique()
st.write(df)

# Sidebar
st.sidebar.title('Options')
st.sidebar.subheader('Timeseries options')
feature_section = st.sidebar.multiselect(label='features to plot', options=numeric_cols)
coins_dropdown = st.sidebar.selectbox(label='Coins Ticker', options=unique_coins)

# Pyplot
df = df[df['coin_symbol']==coins_dropdown]
df_features = df[feature_section]
plotly_fig = px.line(data_frame=df_features, x=df_features.index, y=feature_section, title=(str(coins_dropdown) + " " + "timeline"))
st.plotly_chart(plotly_fig)
