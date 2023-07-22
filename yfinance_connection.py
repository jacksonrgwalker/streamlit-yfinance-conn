import pandas as pd
import streamlit as st
import yfinance as yf
from streamlit.connections import ExperimentalBaseConnection


class YahooFinanceConnection(ExperimentalBaseConnection[yf.Ticker]):
    """
    A connection to Yahoo Finance.
    Takes a single stock ticker symbol as a parameter and returns a yfinance.Ticker object.
    """

    def _connect(self, **kwargs) -> yf.Ticker:
        if "ticker" in kwargs:
            self.ticker_str = kwargs.pop("ticker")
        else:
            self.ticker_str = self._secrets["ticker"]

        return yf.Ticker(self.ticker_str)

    def ticker(self) -> yf.Ticker:
        return self._instance

    def query(self, ttl: int = 3600, **kwargs) -> pd.DataFrame:
        """
        Wraps the Ticker.history() method.

        :Parameters:
            period : str
                Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
                Either Use period parameter or use start and end
            interval : str
                Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                Intraday data cannot extend last 60 days
            start: str
                Download start date string (YYYY-MM-DD) or _datetime, inclusive.
                Default is 99 years ago
                E.g. for start="2020-01-01", the first data point will be on "2020-01-01"
            end: str
                Download end date string (YYYY-MM-DD) or _datetime, exclusive.
                Default is now
                E.g. for end="2023-01-01", the last data point will be on "2022-12-31"
            prepost : bool
                Include Pre and Post market data in results?
                Default is False
            auto_adjust: bool
                Adjust all OHLC automatically? Default is True
            back_adjust: bool
                Back-adjusted data to mimic true historical prices
            repair: bool or "silent"
                Detect currency unit 100x mixups and attempt repair.
                If True, fix & print summary. If "silent", just fix.
                Default is False
            keepna: bool
                Keep NaN rows returned by Yahoo?
                Default is False
            proxy: str
                Optional. Proxy server URL scheme. Default is None
            rounding: bool
                Round values to 2 decimal places?
                Optional. Default is False = precision suggested by Yahoo!
            timeout: None or float
                If not None stops waiting for a response after given number of
                seconds. (Can also be a fraction of a second e.g. 0.01)
                Default is 10 seconds.
            debug: bool
                If passed as False, will suppress message printing to console.
                DEPRECATED, will be removed in future version
            raise_errors: bool
                If True, then raise errors as Exceptions instead of logging.
        """

        @st.cache_data(ttl=ttl)
        def _query(ticker_str, **kwargs) -> pd.DataFrame:
            # add the ticker_str to the kwargs
            # so that we update the cache when the ticker changes
            # there is probably a better way to do this
            # but I just want a hoody and I have finals to study for
            ticker = self.ticker()
            return ticker.history(**kwargs)

        return _query(self.ticker_str, **kwargs)

    def history(self, **kwargs) -> pd.DataFrame:
        """
        Wraps the Ticker.history() method.

        :Parameters:
            period : str
                Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
                Either Use period parameter or use start and end
            interval : str
                Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                Intraday data cannot extend last 60 days
            start: str
                Download start date string (YYYY-MM-DD) or _datetime, inclusive.
                Default is 99 years ago
                E.g. for start="2020-01-01", the first data point will be on "2020-01-01"
            end: str
                Download end date string (YYYY-MM-DD) or _datetime, exclusive.
                Default is now
                E.g. for end="2023-01-01", the last data point will be on "2022-12-31"
            prepost : bool
                Include Pre and Post market data in results?
                Default is False
            auto_adjust: bool
                Adjust all OHLC automatically? Default is True
            back_adjust: bool
                Back-adjusted data to mimic true historical prices
            repair: bool or "silent"
                Detect currency unit 100x mixups and attempt repair.
                If True, fix & print summary. If "silent", just fix.
                Default is False
            keepna: bool
                Keep NaN rows returned by Yahoo?
                Default is False
            proxy: str
                Optional. Proxy server URL scheme. Default is None
            rounding: bool
                Round values to 2 decimal places?
                Optional. Default is False = precision suggested by Yahoo!
            timeout: None or float
                If not None stops waiting for a response after given number of
                seconds. (Can also be a fraction of a second e.g. 0.01)
                Default is 10 seconds.
            debug: bool
                If passed as False, will suppress message printing to console.
                DEPRECATED, will be removed in future version
            raise_errors: bool
                If True, then raise errors as Exceptions instead of logging.
        """
        return self.query(**kwargs)

    def get_long_name(self):
        """
        Returns the long name of the company, if available.
        """
        return self.ticker().info.get("longName")