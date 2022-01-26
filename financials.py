import utils
import pandas as pd
import streamlit as st
from yahoo_fin import stock_info

def run(selected_ticker):
    _,col_title,_ = st.columns([3,1,3])

    with col_title:
        st.title("Financial")
    
    if selected_ticker != "No Selection":
        st.subheader(utils.get_company_name(selected_ticker))

        cols = st.columns([2,4,1])
        # Dropdown to select financial analysis
        financial_info = cols[0].selectbox("Select Financial Analysis", ["Income Statement", "Balance Sheet", "Cash Flow"])
        # Dropdown to select time period
        time_period = cols[2].selectbox("Period of Time", ["Annual", "Quarterly"])
        # Bool variable that sets yearly to true or false in case quarterly
        yearly = True if time_period == "Annual" else False 
        data = stock_info.get_income_statement(selected_ticker, yearly = yearly)

        if financial_info == "Income Statement":
            data = stock_info.get_income_statement(selected_ticker, yearly = yearly)
        elif financial_info == "Balance Sheet":
            data = stock_info.get_balance_sheet(selected_ticker, yearly= yearly)
        elif financial_info == "Cash Flow":
            data = stock_info.get_cash_flow(selected_ticker, yearly= yearly)

        df = pd.DataFrame(list(data.items()))

        val_dict = {}

        for i in range(len(df)):
            val_dict[df.iloc[i,0].strftime('%Y-%m-%d')] = [f"{val:,}" if utils.is_numeric(str(val)) else val for val in df.iloc[i,1].values]
       
        df_result = pd.DataFrame(val_dict)
        df_result.index = df.iloc[0,1].index

        st.dataframe(df_result, height = 1000)