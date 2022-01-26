import utils
import streamlit as st
import pandas as pd
import datetime as dt
from yahoo_fin import stock_info
import plotly.graph_objects as go
from plotly.subplots import make_subplots

timespan = ["1M","3M","6M","YTD","1Y","3Y","5Y","MAX"]

def run(selected_ticker):
    _,col_title,_ = st.columns(3)
    with col_title:
        st.title("Summary")
    if selected_ticker != "No Selection":
        st.subheader(utils.get_company_name(selected_ticker))
        st.caption("Current stock price")
        curr_price = str(round(stock_info.get_live_price(selected_ticker), 2))
        st.markdown(f"<h4 style='font-weight: bold; color: navy;'>{curr_price}</h4>", unsafe_allow_html=True)

        # Retrieve stock summary
        summary_info = stock_info.get_quote_table(selected_ticker, dict_result = False)
        # Parsing df values to string
        summary_info["attribute"] = summary_info["attribute"].astype(str)
        summary_info["value"] = summary_info["value"].astype(str)

        # Assigning first column as index and splitting data into two
        df_1 = pd.DataFrame(summary_info.iloc[:9,1])
        df_1.index = summary_info.iloc[:9,0]

        df_2 = pd.DataFrame(summary_info.iloc[9:,1])
        df_2.index = summary_info.iloc[9:,0]

        # Setting start and end datetime
        start_date = utils.set_timespan(30)
        end_date = utils.get_today().now().strftime('%m/%d/%Y')

        # Creating buttons based on timespan array length 
        btn_cols = st.columns(len(timespan)+1)
        btn_cols[0].caption("Select Timespan")

        for i in range(1,len(btn_cols)):
            if btn_cols[i].button(timespan[i-1]):
                start_date = utils.set_timespan(timespan[i-1])
        # Fetching stock data for selected ticker and timespan
        stock_price = utils.get_stock_data(selected_ticker, start_date, end_date)
        # Creating plot based on fetched data 
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        # Add traces
        fig.add_trace(
            go.Scatter(x=stock_price.index, y=stock_price["close"], name="Close Values", 
            fill='tonexty',
            mode='lines', line_color='indigo'),
            secondary_y=False,
            
        )
        # Creating secondary graph
        fig.add_trace(go.Bar(x=stock_price.index, y= stock_price["volume"], name="Volume", marker_color = "lawngreen"), secondary_y = True)
        # Renaming labels 
        fig.update_yaxes(title_text="<b>Volume</b>", range=[0,stock_price["volume"].max()*7], secondary_y=True)
        fig.update_yaxes(title_text="<b>Close Values (USD)</b>", secondary_y=False)
        # Resizing chart
        fig.update_layout( autosize=True, width=900,height=500)
        # Displaying graph on Streamlit
        st.plotly_chart(fig)
        
        # Displaying summary values in two columns
        _,col_lbl,_ = st.columns(3)
        col_lbl.subheader("Stock Info")
        col1, col2= st.columns(2)
        with col1:
            st.dataframe(df_1, 450, 1000)
        with col2:
            st.dataframe(df_2, 450, 1000)

    else:
        _,col_warning,_ = st.columns([1,3,1])
        with col_warning:
            st.markdown("<h3 style='text-align: center; color: gray;'>Please select a ticker to display info</h3>", unsafe_allow_html=True)
