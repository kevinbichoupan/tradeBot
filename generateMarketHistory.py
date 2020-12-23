"""
Create Market History Data Script
"""

from td_ameritrade_api_service import *
import pandas as pd
import datetime
import sqlite3


def pullEquityHistory(symbol: str):
	
	TDAPI = TDAPIService()
	x = TDAPI.getPriceHistory(symbol)
	
	data1 = pd.DataFrame(x['candles'])
	data1['symbol'] = x['symbol']
	data1['date'] = data1['datetime'].apply(lambda x: datetime.datetime.fromtimestamp(x/1000).strftime('%Y-%m-%d'))

	data1 = data1.drop(columns = ['datetime'])


	return data1


def insertEquityHistory(dataframe):
	df = dataframe

	database_name = 'Algotrade_DB.db'
	database = '/Users/kevinbichoupan/Algotrade/Files/' + database_name
	conn = sqlite3.connect(database)
	c = conn.cursor()

	df.to_sql(name = 'equity_history_daily', con = conn, if_exists='append',index=False)
	c.commit()
	conn.close()






if __name__ == '__main__':
	symbol = 'MSFT'
	x = pullEquityHistory(symbol)
	print('\n\n\nEquity History Data Pulled for ' + symbol +'\n\n\n')
	print(x.head())	


	#insertEquityHistory(x)
	#print('Equity History Successfully Written to Algotrade_DB.equity_history_daily\n\n\n')



