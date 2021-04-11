"""

Database Initialize Script

"""



import sqlite3
import configparser
import sys

def createPortfolioTables(portfolioIndex : str):
	
	config = configparser.ConfigParser()
	config.read('/Users/kevinbichoupan/projects/tradeBot/config.conf')
	databaseConfigs = dict(config.items('SQLite3 Database'))

	equity_daily_history_table_name = "equity_history_daily_raw_" + portfolioIndex
	fundamental_table_name = "fundamental_data_raw_" + portfolioIndex


	createEquityHistoryDailyRaw = """
	CREATE TABLE IF NOT EXISTS """ + equity_daily_history_table_name + """  (
		symbol TEXT
		,date TEXT
		,close REAL
		,high REAL
		,low REAL
		,open REAL
		,volume INT
		,PRIMARY KEY (symbol, date)
	);"""

	createFundamentalDataRaw = """
	CREATE TABLE IF NOT EXISTS """ + fundamental_table_name + """ (
		date TEXT
		,symbol TEXT
		,description TEXT
		,exchange TEXT
		,assetType TEXT
		,beta REAL
		,bookValuePerShare REAL
		,currentRatio REAL
		,divGrowthRate3Year REAL
		,dividendAmount REAL
		,dividendDate TEXT
		,dividendYield REAL
		,epsChange REAL
		,epsChangePercentTTM REAL
		,epsTTM REAL
		,grossMarginMRQ REAL
		,grossMarginTTM REAL
		,interestCoverage REAL
		,marketCap REAL
		,netProfitMarginMRQ REAL
		,netProfitMarginTTM REAL
		,operatingMarginMRQ REAL
		,operatingMarginTTM REAL
		,pbRatio REAL
		,pcfRatio REAL
		,peRatio REAL
		,pegRatio REAL
		,prRatio REAL
		,quickRatio REAL
		,returnOnAssets REAL
		,returnOnEquity REAL
		,returnOnInvestment REAL
		,revChangeIn REAL
		,revChangeTTM REAL
		,revChangeYear REAL
		,sharesOutstanding INT
		,totalDebtToCapital REAL
		,totalDebtToEquity REAL
		,PRIMARY KEY (date, symbol)
	);
	"""


	database_info = {
		'database_location' : databaseConfigs['database_location']
		,'portfolio' : portfolioIndex
		,'historical_table' : equity_daily_history_table_name
		,'fundamental_table' : fundamental_table_name
	}


	try:
	
		print('INITIALIZING - databaseInitializeScript.py')
		print('Database creation for portflio ' + portfolioIndex)
		
		conn = sqlite3.connect(databaseConfigs['database_location'])
		c = conn.cursor()
		print('Connection to Database Successful')

		c.execute(createEquityHistoryDailyRaw)
		print('Created Historical Table -  ' + database_info['historical_table'])

		c.execute(createFundamentalDataRaw)
		print('Created Fundamental Table - ' + database_info['fundamental_table'])

		print('COMPLETED - databaseInitializeScript.py')

		c.close()

		return database_info

	except:
		print('ERROR - databaseInitializeScript.py')


if __name__ == '__main__':
	print('\n\n\n')
	createPortfolioTables(str(sys.argv[1]))
	print('\n\n\n')







