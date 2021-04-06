"""
Generate Fundamental Data Script
"""


from tdAmeritradeAPIService import *
import pandas as pd
import numpy as np
import datetime
import sqlite3
import sys



def pullFundamentals(symbol: str):
	
	TDAPI = TDAPIService()
	x = TDAPI.getFundamentals(symbol)
	
	data1 = pd.DataFrame(x[symbol]).reset_index()
	data1.columns = ['metric', 'value', 'cusip', 'symbol', 'description', 'exchange', 'assetType']
	
	fundamentalHeader = ['symbol', 'description', 'exchange', 'assetType']	
	fundamentalHeaderData = data1[fundamentalHeader].iloc[[0]]

	data1.index = [0]*len(data1)
	data2 = data1.pivot(index = None, columns = 'metric', values = 'value')
	
	data3 = fundamentalHeaderData.merge(data2)
	data3['date'] = datetime.datetime.today().strftime('%Y-%m-%d')

	data3 = data3[['date', 'symbol', 'description', 'exchange', 'assetType', 'beta', 'bookValuePerShare', 'currentRatio', 'divGrowthRate3Year', 'dividendAmount', 'dividendDate', 'dividendYield', 'epsChange', 'epsChangePercentTTM', 'epsTTM', 'grossMarginMRQ', 'grossMarginTTM', 'interestCoverage', 'marketCap', 'netProfitMarginMRQ', 'netProfitMarginTTM', 'operatingMarginMRQ', 'operatingMarginTTM', 'pbRatio', 'pcfRatio', 'peRatio', 'pegRatio', 'prRatio', 'quickRatio', 'returnOnAssets', 'returnOnEquity', 'returnOnInvestment', 'revChangeIn', 'revChangeTTM', 'revChangeYear', 'sharesOutstanding', 'totalDebtToCapital', 'totalDebtToEquity']]

	return data3
		


def checkIfFundamentalsExists(symbol:str):
	
	database_name = 'tradeBot_DW.db'
	database = '/Users/kevinbichoupan/projects/tradeBot/Files/' + database_name
	conn = sqlite3.connect(database)
	c = conn.cursor()
	query = "select max(date) from fundamental_data_raw where symbol  = '" + symbol + "';"
	x = c.execute(query).fetchall()
	conn.close()

	currentDate = datetime.datetime.today().strftime('%Y-%m-%d')

	try:
		a = x[0][0]
	except:
		a = x

	return a == currentDate

	 

def insertCurrentFundamentalData(symbol:str):
	
	currentDate = datetime.datetime.today().strftime('%Y-%m-%d')
	
	if not checkIfFundamentalsExists(symbol):
		print('Inserting ' + symbol + ' Fundamental Data for ' + currentDate) 

		data1 = pullFundamentals(symbol)
		
		database_name = 'tradeBot_DW.db'
		database = '/Users/kevinbichoupan/projects/tradeBot/Files/'+database_name
		conn = sqlite3.connect(database)
		c = conn.cursor()

		try:
			data1.to_sql('fundamental_data_raw', conn, if_exists = 'append', index = False)
			print('Data inserted successfully')
		except:
			print('Data not inserted successfully')

	else:
		print('Fundamental data for ' + symbol + ' as of ' + currentDate + ' not inserted successfully')



if __name__ == '__main__':
	#pullFundamentals('MSFT')
	#print(checkIfFundamentalsExists('MSFT', datetime.datetime.today().strftime('%Y-%m`-%d')))
	print('\n\n\n')
	insertCurrentFundamentalData(str(sys.argv[1]))
	print('\n\n\n')	
	
