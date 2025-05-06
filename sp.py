import streamlit as st
import pandas as pd
import plotly.express as px

# App Config
st.set_page_config(page_title="Advanced Stock Analyzer", layout="wide")

# Load and cache data
@st.cache_data
def load_data():
    df = pd.read_csv("IFA.csv")
    df = df.drop("Unnamed: 0", axis=1)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# Sidebar - Controls
st.sidebar.title("Filters & Options")

# Stock selection
stock_options = df['Symbol'].unique().tolist()
selected_stocks = st.sidebar.multiselect("Select Stock(s)", stock_options, default=stock_options[:1])

# Date selection
min_date = df['Date'].min()
max_date = df['Date'].max()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

# Moving average checkbox
show_ma = st.sidebar.checkbox("Show Moving Average", value=False)
ma_window = st.sidebar.slider("MA Window (days)", 5, 50, 20) if show_ma else None

# Filter data
filtered_df = df[(df['Symbol'].isin(selected_stocks)) &
                 (df['Date'] >= pd.to_datetime(date_range[0])) &
                 (df['Date'] <= pd.to_datetime(date_range[1]))]

# Apply moving average if selected
if show_ma:
    filtered_df['MA'] = filtered_df.groupby('Symbol')['Close'].transform(lambda x: x.rolling(ma_window).mean())

# Title
st.title("📈 Advanced Stock Closing Price Visualizer")

# Plotting
st.subheader("Stock Price Chart")
fig = px.line(filtered_df,
              x='Date',
              y='MA' if show_ma else 'Close',
              color='Symbol',
              title="Stock Price Over Time",
              labels={'value': 'Price', 'Date': 'Date'},
              markers=True)
st.plotly_chart(fig, use_container_width=True)

# Summary stats
st.subheader("📊 Summary Statistics")
st.write(filtered_df.groupby("Symbol")[['Open', 'Close', 'High', 'Low', 'Volume']].describe().round(2))

# Raw Data Preview
with st.expander("🔍 View Raw Data"):
    st.dataframe(filtered_df.sort_values(by='Date', ascending=False), use_container_width=True)
