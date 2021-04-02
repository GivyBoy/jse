import pandas as pd 
import numpy as np
from datetime import date
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


def get_jse_data_daily_returns(ticker, start_date = '2000-01-01', end_date = date.today()):
    """
    This aim of this function is to scrape stock data from the Jamaica Stock Exchange. 
    
    ticker: Enter the ticker of the stock you wish to analyze
    start_date: in the format 'yyyy-mm-dd', enter the starting date if the data you want.
    end_date: The default end date is today (yes, I coded it to be dynamic). If you want a special date, enter that date in the format 'yyy-mm-dd'.
    
    """
    
    ticker = ticker.upper() #Ensures that all the letters of the ticker are capitalized. This is to ensure that the code doesn't get any errors later on, since tickers are normallt all caps.
    
    #Catches an error if the user forgets to input the start date and uses of the fault value of January 1, 2017.
    if start_date:
        start_date = pd.to_datetime(start_date, format='%Y%m%d', errors='ignore') #formats the date
    else:
        start_date = '2000-01-01'
    
    #same as above 
    if end_date:
        end_date = pd.to_datetime(end_date, format='%Y%m%d', errors='ignore') #formats the date
    else:
        end_date = date.today()
    
    data = pd.read_html(f"""https://www.jamstockex.com/market-data/download-data/price-history/{ticker}/{start_date}/{end_date}""") #The Jamaica Stock Exchange has a pattern with how they store their data. I found that pattern, as such, I'm leveraging it. This line scrapes the data from the JSE and tries to return it as a dataframe.
    
    data = data[0] #The data wasn't returned as a dataframe, instead, it was returned as an array with one element: the data. This line indexes into the array amd accesses the data.
    
    del data['Unnamed: 0'] #deletes an unnecessary row
    
    data.index = data['Date'] #assigns the "Date" column as the index
    
    del data['Date'] #deletes the row
    
    data.index = pd.to_datetime(data.index) #transforms the dates into a datetime object. Most libraries need the index to be a datetime object, so that's why this was done.
    
    for i, b in enumerate(data.columns.values):
        data.columns.values[i] = b.replace(" ($)", "").replace("  ", " ") #The titles of the columns aren't formatted properly, so these lines correct that.
        
    data = data.dropna(axis=1) #removes all the columns that don't have useful values
    
    data = data['Close Price'] 
    data = data.pct_change()
    
    return data #returns the datarame to the user 

def get_jse_data(ticker, start_date = '2000-01-01', end_date = date.today()):
    """
    This aim of this function is to scrape stock data from the Jamaica Stock Exchange. 
    
    ticker: Enter the ticker of the stock you wish to analyze
    start_date: in the format 'yyyy-mm-dd', enter the starting date if the data you want.
    end_date: The default end date is today (yes, I coded it to be dynamic). If you want a special date, enter that date in the format 'yyy-mm-dd'.
    
    """
    
    ticker = ticker.upper() #Ensures that all the letters of the ticker are capitalized. This is to ensure that the code doesn't get any errors later on, since tickers are normally all caps.
    
    #Catches an error if the user forgets to input the start date and uses of the fault value of January 1, 2017.
    if start_date:
        start_date = pd.to_datetime(start_date, format='%Y%m%d', errors='ignore') #formats the date
    else:
        start_date = '2000-01-01'
    
    #same as above 
    if end_date:
        end_date = pd.to_datetime(end_date, format='%Y%m%d', errors='ignore') #formats the date
    else:
        end_date = date.today()
    
    data = pd.read_html(f"""https://www.jamstockex.com/market-data/download-data/price-history/{ticker}/{start_date}/{end_date}""") #The Jamaica Stock Exchange has a pattern with how they store their data. I found that pattern, as such, I'm leveraging it. This line scrapes the data from the JSE and tries to return it as a dataframe.
    
    data = data[0] #The data wasn't returned as a dataframe, instead, it was returned as an array with one element: the data. This line indexes into the array amd accesses the data.
    
    del data['Unnamed: 0'] #deletes an unnecessary row
    
    data.index = data['Date'] #assigns the "Date" column as the index
    
    del data['Date'] #deletes the row
    
    data.index = pd.to_datetime(data.index) #transforms the dates into a datetime object. Most libraries need the index to be a datetime object, so that's why this was done.
    
    for i, b in enumerate(data.columns.values):
        data.columns.values[i] = b.replace(" ($)", "").replace("  ", " ") #The titles of the columns aren't formatted properly, so these lines correct that.
        
    data = data.dropna(axis=1) #removes all the columns that don't have useful values
    
    return data['Close Price'] #returns the datarame to the user 

def drawdown(return_series: pd.Series):
    """Takes a time series of asset returns.
       returns a DataFrame with columns for
       the wealth index, 
       the previous peaks, and 
       the percentage drawdown
    """
    wealth_index = 1000*(1+return_series).cumprod()
    previous_peaks = wealth_index.cummax()
    drawdowns = (wealth_index - previous_peaks)/previous_peaks
    return pd.DataFrame({"Wealth": wealth_index, 
                         "Previous Peak": previous_peaks, 
                         "Drawdown": drawdowns})