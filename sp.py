import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# Page config (optional)
st.set_page_config(page_title="Stock Viewer", layout="wide")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("IFA.csv")
    df = df.drop("Unnamed: 0", axis=1)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# Sidebar for stock selection
st.sidebar.title("Stock Filter")
stock_list = df['Symbol'].unique()
selected_stock = st.sidebar.selectbox("Select a Stock Symbol", stock_list)

# Filter the data
stk = df[df['Symbol'] == selected_stock]

# Title
st.title(f"{selected_stock} Stock Closing Price Over Time")

# Plotting
fig, ax = plt.subplots(figsize=(10, 5))
sb.lineplot(x=stk['Date'], y=stk['Close'], ax=ax)
plt.xticks(rotation=90)
ax.set_xlabel("Date")
ax.set_ylabel("Close Price")
ax.set_title(f"Closing Price of {selected_stock}")
st.pyplot(fig)
