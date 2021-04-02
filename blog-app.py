import streamlit as st 
import seaborn as sns
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import datetime
import jse as j
st.set_option('deprecation.showPyplotGlobalUse', False)

html_temp = """ 
    <div style ="padding:15px"> 
    <h1 style ="text-align:center;font-size:40px">JSE (Jamaica Stock Exchange) Web Application</h1> 
    <h6 style ="text-align:center;font-size:15px">Created by Anthony Givans</h6> 
    </div> 
    """
      
st.markdown(html_temp, unsafe_allow_html = True) 
st.write("""## You are now able to visualize the stock data of Jamaican companies, along with some other key metrics, with relative ease.""")
st.write('')
st.write("""All of the data has been gathered directly from the Jamaica Stock Exchange :)""")

ticker = st.text_input("Enter the stock ticker here (for example, 'BIL' for Barita Investments Limited): ").upper()
st.write('')
if st.button('Submit'):
    st.cache()
    stock_price = j.get_jse_data(ticker)
    st.write('')

    
    plt.figure(figsize=(16,8))    
    plt.plot(stock_price, linewidth= 0.8, color='green')
    plt.fill_between(stock_price.index, stock_price, color='g', alpha=0.4)
    plt.ylim(0)
    plt.grid(True)
    st.pyplot()
    with st.beta_expander("See explanation"):
        st.write(f"""The chart above shows the stock price of {ticker}. """)
    st.write('')
    st.write('')

    returns = j.get_jse_data_daily_returns(ticker)
    col = []
    for val in returns.values:
        if float(val) > 0:
            col.append('green')
        else:
            col.append('red')

    plt.figure(figsize=(12,6))        
    plt.bar(returns.index, returns.values, color = col, width=15)
    st.pyplot()
    with st.beta_expander("See explanation"):
        st.write("""This chart shows the daily fluctuations of the stock's price. If you see a lot of green and not much red, the stock has been performing really well :) """)
    st.write('')
    
    data_processed = [i for i in returns if i!=0]
    sns.displot(data=data_processed, kde=True, bins=80, color='green', alpha=0.4, height=6, aspect=2)
    st.pyplot()
    with st.beta_expander("See explanation"):
        st.write("""This chart shows the distribution of the fluctuations of the stock price. If most of the negative fluctuations are concentrated between 0 and -0.1, it's a good thing. It means that, statistically, when the stock price is drecreasing, it won't decrease by much. Also, note that I removed all non-changes (zeroes). """)
    st.write('')

    
    drawdown = j.drawdown(returns)
    plt.figure(figsize=(12,6))
    plt.title('Drawdown')
    drawdown['Drawdown'].plot(color='red', linewidth= 0.8,).autoscale(axis='x', tight=True)
    plt.fill_between(drawdown.index, drawdown['Drawdown'],color='r', alpha=0.4)
    plt.grid(True)
    st.pyplot()
    with st.beta_expander("See explanation"):
        st.write("""This chart shows how much (as a percent of the most recent high) of the stock price has been wiped out, due to market forces.""")
    st.write('')

    wealth_index = 1000*(1+returns).cumprod()
    plt.plot(wealth_index, linewidth= 0.8,  color='green')
    plt.fill_between(wealth_index.index, wealth_index, color='g',alpha=0.4)
    plt.ylim(0)
    plt.grid(True)
    st.pyplot()
    with st.beta_expander("See explanation"):
        st.write("""This chart shows your returns if you invested $1000 on the first day the stock entered the market.""")






