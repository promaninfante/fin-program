
import utils 
import pandas as pd
import streamlit as st
from yahoo_fin import stock_info

def run(selected_ticker):
    _,col_title,_ = st.columns([3,1,3])

    with col_title:
        st.title("Statistics")
    
    if selected_ticker != "No Selection":
        st.subheader(utils.get_company_name(selected_ticker))

        statistics_headers = {
            "Fiscal Year": ["Fiscal Year Ends", "Most Recent Quarter (mrq)"], 
            "Profitability": ["Profit Margin", "Operating Margin (ttm)"],
            "Management Effectiveness": ["Return on Assets (ttm)", "Return on Equity (ttm)"],
            "Income Statement": ["Revenue (ttm)", "Revenue Per Share (ttm)", 
            "Quarterly Revenue Growth (yoy)", "Gross Profit (ttm)", "EBITDA", "Net Income Avi to Common (ttm)",
            "Diluted EPS (ttm)", "Quarterly Earnings Growth (yoy)"],
            "Balance Sheet": ["Total Cash (mrq)", "Total Cash Per Share (mrq)", "Total Debt (mrq)", "Total Debt/Equity (mrq)",
            "Current Ratio (mrq)", "Book Value Per Share (mrq)"],
            "Cash Flow Statement": ["Operating Cash Flow (ttm)", "Levered Free Cash Flow (ttm)"],
            "Stock Price History": ["Beta (5Y Monthly)", "52-Week Change 3", "S&P500 52-Week Change 3", "52 Week High 3", 
            "52 Week Low 3", "50-Day Moving Average 3", "200-Day Moving Average 3"],
            "Share Statistics": ["Avg Vol (3 month) 3", "Avg Vol (10 day) 3", "Shares Outstanding 5", "Implied Shares Outstanding 6",
            "Float 8", "% Held by Insiders 1", "% Held by Institutions 1", "Shares Short (Oct 28, 2021) 4", 
            "Short Ratio (Oct 28, 2021) 4", "Short % of Float (Oct 28, 2021) 4", "Short % of Shares Outstanding (Oct 28, 2021) 4",
            "Shares Short (prior month Sep 29, 2021) 4"],
            "Dividends & Splits": ["Forward Annual Dividend Rate 4", "Forward Annual Dividend Yield 4", "Trailing Annual Dividend Rate 3",
            "Trailing Annual Dividend Yield 3", "5 Year Average Dividend Yield 4", "Payout Ratio 4", "Dividend Date 3",
            "Ex-Dividend Date 4", "Last Split Factor 2", "Last Split Date 3"]
        }
        # Extract Stats Info
        data = stock_info.get_stats(selected_ticker)
        df = pd.DataFrame(list(data.items()))
        attribute_df = df.iloc[0,1]
        # Extract valuation info
        valuation_data = stock_info.get_stats_valuation(selected_ticker)
        valuation_df =  pd.DataFrame(list(valuation_data.items()))

        valu_attr_df = valuation_df.iloc[0,1]
        valuation_dict = {}
        for ind in range(len(valu_attr_df)):
            valuation = valu_attr_df[ind]
            val = valuation_df.iloc[1,1][ind]
            valuation_dict[valuation] = val
        print(valuation_dict)
        df_valuation = pd.DataFrame.from_dict(valuation_dict, orient="index")

        stats_dict = {"Valuation Measures": df_valuation}

        for i in range(len(statistics_headers.keys())):
            header = list(statistics_headers)[i]
            # Getting each sections array from header
            arr_stats = list(statistics_headers.values())[i]
            section_dict = {}
            for stat in range(len(arr_stats)):
                # Creating dict with value of each stat in section
                section_name = arr_stats[stat]
                # Get index of current section in attributes df 
                if attribute_df[attribute_df == section_name].empty:
                    next
                
                index = attribute_df[attribute_df == section_name].index[0]
                # Retrieve value in df 
                val = df.iloc[1,1][index]
                # Value fetched
                section_dict[section_name] = val 

            stats_dict[header] = pd.DataFrame.from_dict(section_dict, orient="index")
        stats_df = pd.DataFrame(list(stats_dict.items()))

        col1, col2 = st.columns(2)
        with col1:
            for i in range(5):
                st.subheader(stats_df.iloc[:,0][i])
                # Each analysis dataframe is in second col
                stat = stats_df.iloc[:,1][i]
                # Assigning param name as index
                param = stat.iloc[:,1:]
                param.index = stat.iloc[:,0]
                # Displaying table from dataframe
                st.dataframe(stat)
        with col2:
            for i in range(5,10):
                st.subheader(stats_df.iloc[:,0][i])
                # Each analysis dataframe is in second col
                stat = stats_df.iloc[:,1][i]
                # Assigning param name as index
                param = stat.iloc[:,1:]
                param.index = stat.iloc[:,0]
                # Displaying table from dataframe
                st.dataframe(stat)           
    else:
        _,col_warning,_ = st.columns([1,3,1])
        with col_warning:
            # st.subheader("Please select a ticker to display info")
            st.markdown("<h3 style='text-align: center; color: gray;'>Please select a ticker to display info</h3>", unsafe_allow_html=True)

        