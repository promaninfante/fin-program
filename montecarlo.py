import utils
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def run(selected_ticker):
    _,col_title,_ = st.columns([3,2,3])

    with col_title:
        st.title("MonteCarlo")

    if selected_ticker != "No Selection":
        st.subheader(utils.get_company_name(selected_ticker))
        cols = st.columns([2,4,1])
        # Dropdown to select number of simulations
        nbr_simulations = cols[0].selectbox("No. of Simulations", ["200", "500", "1000"])
        # Dropdown to select time period
        time_horizon = cols[2].selectbox("Time Horizon (days)", ["30", "60", "90"])
        start_date = utils.set_timespan("1Y")
        end_date = utils.get_today().strftime('%m/%d/%Y')
        np.random.seed(123)

        # CODE REFERENCE: Financial Programming class, section 3
        data = utils.get_stock_data(selected_ticker, start_date, end_date)
        close_price = data["close"]
        daily_return = close_price.pct_change()
        daily_volatility = np.std(daily_return)

        df_montecarlo = pd.DataFrame()
        for i in range(int(nbr_simulations)):
            next_price = []
            last_price = close_price[-1]

            for x in range(int(time_horizon)):
                # Get random percentage around mean and std
                future_return = np.random.normal(0, daily_volatility)
                # Random future price
                future_price = last_price * (1 + future_return)
                # Save the price and go to next day
                next_price.append(future_price)
                last_price = future_price
            df_montecarlo[i] = next_price
        
        # Creating plot based on fetched data 
        fig, ax = plt.subplots(figsize=(15,10))
        # Plotting the adjclose column
        ax.plot(df_montecarlo)
        plt.title(f'Monte Carlo simulation for {selected_ticker} stock price in next {time_horizon} days')
        plt.xlabel('Day')
        plt.ylabel('Price')
        plt.axhline(y=close_price[-1], color='red')
        plt.legend(['Current stock price is: ' + str(np.round(close_price[-1], 2))])
        ax.get_legend().legendHandles[0].set_color('red')
        st.caption(f"Value at Risk 95% confidence: USD {get_value_at_risk(df_montecarlo, close_price[-1])}")
        st.pyplot(fig)
    
    else:
        _,col_warning,_ = st.columns([1,3,1])
        with col_warning:
            # st.subheader("Please select a ticker to display info")
            st.markdown("<h3 style='text-align: center; color: gray;'>Please select a ticker to display info</h3>", unsafe_allow_html=True)

def get_value_at_risk(sim_df, last_price):
        # Price at 95% confidence interval
        future_price_95ci = np.percentile(sim_df.iloc[-1:, :].values[0, ], 5)

        # Value at Risk
        VaR = last_price - future_price_95ci
        return  str(np.round(VaR, 2)) 