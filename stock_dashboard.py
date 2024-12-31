import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# Set the title of the web app
st.title("📈 Stock Market Analysis Dashboard")

# Sidebar for user inputs
st.sidebar.header("User Input")

# Stock selection
selected_stock = st.sidebar.selectbox(
    "Select a stock", 
    ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']
)

# Date range selection
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime('2023-01-01'))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime('today'))

# Ensure the start date is before the end date
if start_date > end_date:
    st.sidebar.error("Error: End date must fall after start date.")

# Function to load stock data with caching
@st.cache_data
def load_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    data.reset_index(inplace=True)
    return data

# Load data based on user inputs
data = load_data(selected_stock, start_date, end_date)

# Display raw data table
st.subheader(f"Raw Data - {selected_stock}")
st.write(data.tail())


# Plot closing price over time
fig = px.line(data, x='Date', y='Close', title=f"{selected_stock} Closing Price Over Time")
st.plotly_chart(fig)

# Plot trading volume
fig2 = px.bar(data, x='Date', y='Volume', title=f"{selected_stock} Trading Volume")
st.plotly_chart(fig2)

st.sidebar.subheader("Download Data")
csv = data.to_csv()
st.sidebar.download_button(label="Download CSV", data=csv, file_name='stock_data.csv', mime='text/csv')

# Display summary statistics
st.subheader(f"Statistics for {selected_stock}")
st.write(data.describe())
