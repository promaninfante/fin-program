import streamlit as st
import summary, chart, statistics, financials, analysis, montecarlo
from st_btn_select import st_btn_select
from yahoo_fin import stock_info

TABS = {
    "Summary": summary,
    "Chart": chart,
    "Statistics": statistics,
    "Financials": financials,
    "Analysis": analysis,
    "Monte Carlo": montecarlo
}

def main():
    # Obtaining all sp500 tickers to display on dropdown list
    sp500 = stock_info.tickers_sp500()
    tickers = ["No Selection"] + sp500
    st.set_page_config(layout="wide")
     
    # Sidebar
    st.sidebar.title("Menu")
    global selected_ticker
    selected_ticker = "No Selection"  
    # CODE REFERENCE: https://github.com/0phoff/st-btn-select
    global page
    page = st_btn_select(
    # Different pages
    (list(TABS.keys())),
    # Enable navbar
    nav=True,
    )
    selected_ticker = st.sidebar.selectbox("Choose an enterprise from the list", tickers)
    update_btn = st.sidebar.button("Update Info")
   
    if page in TABS.keys():
        display_page()

def display_page():
    TABS[page].run(selected_ticker)
    
# Condition to run the main function upon calling 
if __name__ == "__main__":
    main()