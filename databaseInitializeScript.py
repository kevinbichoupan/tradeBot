"""

Database Initialize Script

"""



import sqlite3



database_name = 'tradeBot_DW.db'
database = '/Users/kevinbichoupan/projects/tradeBot/Files/' + database_name
conn = sqlite3.connect(database)
c = conn.cursor()
print('Connection to Database Successful')


createEquityHistoryDailyRaw = """
CREATE TABLE IF NOT EXISTS equity_history_daily_raw (
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
CREATE TABLE IF NOT EXISTS fundamental_data_raw (
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


c.execute(createEquityHistoryDailyRaw)
print('Successfully created table equity_history_daily_raw')
c.execute(createFundamentalDataRaw)
print('Successfully created table fundamental_data_raw')

c.close()

