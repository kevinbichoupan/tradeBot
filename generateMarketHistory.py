"""
Create Market History Data Script
"""

from tdAmeritradeAPIService import *
import pandas as pd
import datetime
import sqlite3
from dateutil.relativedelta import *



def generateDateRangesForEquityHistoryPull(symbol):

	database_name = 'tradeBot_DW.db'
	database = '/Users/kevinbichoupan/projects/tradeBot/Files/' + database_name
	conn = sqlite3.connect(database)
	c = conn.cursor()	
	query = "select max(date) from equity_history_daily_raw where symbol = '" + symbol + "';"
	x = c.execute(query).fetchall()
	conn.close()

	try:
		a = x[0][0]
	except:
		a = x

	dateRanges = []
	minHistoryDate = datetime.datetime(2018,1,1,0,0)
	maxHistoryDate = datetime.datetime.today() - datetime.timedelta(days=1)
	epoch = datetime.datetime.utcfromtimestamp(0)

	if not a:
		monthsGap = (maxHistoryDate.year - minHistoryDate.year) * 12 + (maxHistoryDate.month - minHistoryDate.month)
		
		for i in range(0, monthsGap):
			startTimestampTmp = round(((minHistoryDate + relativedelta(months=i)) - epoch).total_seconds() * 1000)
			endTimestampTmp = round(((maxHistoryDate + relativedelta(months=i+1) - datetime.timedelta(days=1)) - epoch).total_seconds() * 1000)
			dateRanges.append((startTimestampTmp, endTimestampTmp))
		
		startTimestampTmp = round(((minHistoryDate + relativedelta(months = monthsGap)) - epoch).total_seconds() * 1000)
		endTimestampTmp = round((maxHistoryDate - epoch).total_seconds() * 1000)	
		dateRanges.append((startTimestampTmp, endTimestampTmp))
		
		return dateRanges
	else:

	#TODO: add case when there is already history loaded

		return dateRanges
				




def pullEquityHistory(symbol: str, startDate, endDate):
	
	TDAPI = TDAPIService()
	x = TDAPI.getPriceHistory(symbol, startDate, endDate)
	
	data1 = pd.DataFrame(x['candles'])
	data1['symbol'] = x['symbol']
	data1['date'] = data1['datetime'].apply(lambda x: datetime.datetime.fromtimestamp(x/1000).strftime('%Y-%m-%d'))

	data1 = data1.drop(columns = ['datetime'])

	return data1



def insertEquityHistory(symbol):
	
	dateRanges = generateDateRangesForEquityHistoryPull(symbol)	
	
	database_name = 'tradeBot_DW.db'
	database = '/Users/kevinbichoupan/projects/tradeBot/Files/' + database_name
	conn = sqlite3.connect(database)
	
	for i in dateRanges:
		dataHistorySlice = pullEquityHistory(symbol, str(i[0]), str(i[1]))
		print(i)
		dataHistorySlice.to_sql('equity_history_daily_raw', conn, if_exists = 'append', index = False)

	conn.close()










if __name__ == '__main__':

	symbol = 'MSFT'
	insertEquityHistory(symbol)





