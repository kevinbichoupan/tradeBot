"""
Generate Daily Market History Data Script
"""

from tdAmeritradeAPIService import *
import pandas as pd
import datetime
import sqlite3
from dateutil.relativedelta import *
import sys





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
	
	maxHistoryDate = datetime.datetime.today() - datetime.timedelta(days=1)
	epoch = datetime.datetime.utcfromtimestamp(0)
	
	if a == maxHistoryDate.strftime('%Y-%m-%d'):	# RETURN NULL DATERANGES
		print('History is up to date')
		return dateRanges

	elif not a:	#PERFORM FULL HISTORY GENERATION 
		print('Performing Full History Generation')
		minHistoryDate = datetime.datetime(2010,1,1,0,0) + datetime.timedelta(hours=5)
	
	else:	#PERFORM PARTIAL HISTORY GENERATION
		print('Performing Partial History Generation')
		minHistoryDate = datetime.datetime(int(a[0:4]), int(a[5:7]), int(a[8:11])) + datetime.timedelta(days=1) + datetime.timedelta(hours=5)

	monthsGap = (maxHistoryDate.year - minHistoryDate.year) * 12 + (maxHistoryDate.month - minHistoryDate.month)
	
	for i in range(0, monthsGap):
		startTimestampTmp = round(((minHistoryDate + relativedelta(months=i)) - epoch).total_seconds() * 1000)
		endTimestampTmp = round(((minHistoryDate + relativedelta(months=i+1) - datetime.timedelta(days=1)) - epoch).total_seconds() * 1000)
		dateRanges.append((startTimestampTmp, endTimestampTmp))
	
	startTimestampTmp = round(((minHistoryDate + relativedelta(months = monthsGap)) - epoch).total_seconds() * 1000)
	endTimestampTmp = round((maxHistoryDate - epoch).total_seconds() * 1000)	
	dateRanges.append((startTimestampTmp, endTimestampTmp))
	
	return dateRanges








def pullEquityHistory(symbol: str, startDate, endDate):
	
	TDAPI = TDAPIService()
	x = TDAPI.getPriceHistory(symbol, startDate, endDate)
	try:	
		data1 = pd.DataFrame(x['candles'])
		data1['symbol'] = x['symbol']
		data1['date'] = data1['datetime'].apply(lambda x: datetime.datetime.fromtimestamp(x/1000).strftime('%Y-%m-%d'))

		data1 = data1.drop(columns = ['datetime'])
		return data1
	except:
		return None







def insertEquityHistory(symbol):
	
	dateRanges = generateDateRangesForEquityHistoryPull(symbol)	

	if not dateRanges:
		print('History for ' + symbol + ' is up to date')
		return
	
	database_name = 'tradeBot_DW.db'
	database = '/Users/kevinbichoupan/projects/tradeBot/Files/' + database_name
	conn = sqlite3.connect(database)
	
	for i in dateRanges:
		dataHistorySlice = pullEquityHistory(symbol, str(i[0]), str(i[1]))
		try:
			dataHistorySlice.to_sql('equity_history_daily_raw', conn, if_exists = 'append', index = False)
			print('Successfully inserted data for ' + symbol + ' for date ranges ' + str(i[0]) + ' to ' + str(i[1]))
		except:
			print('No data inserted for ' + symbol + ' for date ranges ' + str(i[0]) + ' to ' + str(i[1]))

	conn.close()










if __name__ == '__main__':
	print('\n\n\n')
	insertEquityHistory(str(sys.argv[1]))
	print('\n\n\n')



