import streamlit as st
from requests.exceptions import HTTPError

from yfinance_connection import YahooFinanceConnection

hackathon_link = "https://discuss.streamlit.io/t/connections-hackathon/47574"
st.title("Yahoo Finance Connection")
st.markdown(f"See the [Connections Hackathon post]({hackathon_link}) for more info.")
st.markdown("Made by [Jackson Walker](https://jwalk.io/)")
st.divider()
col1, col2, col3 = st.columns(3)
ticker_str = col1.text_input("Enter a stock ticker symbol", value="SNOW", key="ticker")
ticker_str = ticker_str.upper()
period = col2.selectbox("Period", ("1y", "6mo", "3mo", "1mo"))
interval = col3.selectbox("Interval", ("1d", "1wk"))

# Create a connection to Yahoo Finance
try:
    conn = st.experimental_connection(
        "yahoo_finance", type=YahooFinanceConnection, ticker=ticker_str
    )

    # Display the company name
    st.text(f"You are pulling data for {conn.get_long_name()}")

    # Pull data from Yahoo Finance
    data = conn.query(period=period, interval=interval)

    # Plot the data
    st.line_chart(data["Close"])

    # Display the data
    st.dataframe(data)

except HTTPError:
    st.error(f"Could not find ticker symbol {ticker_str}", icon="🚨")
    st.stop()
