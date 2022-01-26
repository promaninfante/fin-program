import utils 
import streamlit as st
import pandas as pd
import datetime as dt
from yahoo_fin import stock_info
import plotly.graph_objects as go
from plotly.subplots import make_subplots

timespan = ["1M","3M","6M","YTD","1Y","3Y","5Y","MAX"]
date_range = {
    "Day": "1d",
    "Week": "1wk",
    "Month": "1mo"
}

def run(selected_ticker):
    _,col_title,_ = st.columns(3)
    with col_title:
        st.title("Chart")

    if selected_ticker != "No Selection":
        st.subheader(utils.get_company_name(selected_ticker))

        # Setting default params
        start_date = utils.set_timespan(30)
        end_date = utils.get_today().now().strftime('%m/%d/%Y')

        range_selected = "Day"
        # Creating buttons based on timespan array and 3 extra cols: 
        # label to timespan, to date range and date range dropdown
        btn_cols = st.columns(len(timespan)+1)
        btn_cols[0].caption("Select Timespan")

        for i in range(1,len(btn_cols)):
            if btn_cols[i].button(timespan[i-1]):
                start_date = utils.set_timespan(timespan[i-1])

        opt_cols = st.columns([1,1,4])
        range_selected = opt_cols[0].selectbox("Date Range", list(date_range.keys()))
        graph_type = opt_cols[1].selectbox("Plot Type", ["Line", "Candle"])
        # Fetching stock data for selected ticker and timespan
        stock_price = utils.get_stock_data(selected_ticker, start_date, end_date, interval=date_range[range_selected])

        # Create figure with secondary y-axis 
        # CODE REFERENCE: https://plotly.com/python/multiple-axes/
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        if graph_type == "Line":
            # Add traces
            fig.add_trace(
                go.Scatter(x=stock_price.index, y=stock_price["close"], name="Close Values"),
                secondary_y=False,
            )
            
        elif graph_type == "Candle":
            fig.add_trace(
                go.Candlestick(
                    x=stock_price.index,
                    open=stock_price["open"],
                    high =stock_price["high"],
                    low = stock_price["low"],
                    close = stock_price["close"],
                    name="Candle Values"),
                    secondary_y=False
            )
        # Simple moving average 50 days window size
        # Code REFERENCE: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html
        sma50 = stock_price.close.ewm(span=50, adjust=False).mean()
        
        fig.add_trace(go.Scatter(x=stock_price.index, y= sma50, name = "SMA 50d", line=dict(color='orange', width=1)),  secondary_y = False)
        fig.add_trace(go.Bar(x=stock_price.index, y= stock_price["volume"], name="Volume"), secondary_y = True)
        fig.update_yaxes(title_text="<b>Volume</b>", range=[0,stock_price["volume"].max()*7], secondary_y=True)
        fig.update_yaxes(title_text="<b>Close Values (USD)</b>", secondary_y=False)

        fig.update_layout( autosize=True, width=900,height=650)
        
        st.plotly_chart(fig)
    else:
        _,col_warning,_ = st.columns([1,3,1])
        with col_warning:
            # st.subheader("Please select a ticker to display info")
            st.markdown("<h3 style='text-align: center; color: gray;'>Please select a ticker to display info</h3>", unsafe_allow_html=True)
    