#this shit is supposed to download data for DCF
import yfinance as yf
import pandas as pd

stock = str(input('stock ticker: ')).strip().upper() #TODO: check if it works for all places
ticker = yf.Ticker(stock)
df_is = ticker.financials
df_bs = ticker.balance_sheet
df_cf = ticker.cashflow
combined = pd.concat([df_is,df_bs,df_cf]) #TODO: standardise entries across different reporting formats
combined.to_csv(f'data_for_{stock}.csv') #TODO: write into existing excel