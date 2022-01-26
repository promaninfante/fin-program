import utils
import pandas as pd
import streamlit as st
from yahoo_fin import stock_info

def run(selected_ticker):
    _,col_title,_ = st.columns([3,1,3])

    with col_title:
        st.title("Analysis")
    
    if selected_ticker != "No Selection":
        st.subheader(utils.get_company_name(selected_ticker))

        # Extracting analysts data
        analysis_dict = stock_info.get_analysts_info(selected_ticker)
        # Transforming dictionary into dataframe 
        data = pd.DataFrame(list(analysis_dict.items()))

        # Looping through each dataframe in the dataframe
        for i in range(len(data.iloc[:,1])):
            # Getting each analysis name 
            st.subheader(data.iloc[:,0][i])
            # Each analysis dataframe is in second col
            analysis_df = data.iloc[:,1][i]
            # Assigning param name as index
            analysis = analysis_df.iloc[:,1:]
            analysis.index = analysis_df.iloc[:,0]
            # Displaying table from dataframe
            st.dataframe(analysis)