"""

Trading Algorith - Database Initialize Script

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

c.execute(createEquityHistoryDailyRaw)
print('Successfuly created table equity_history_daily')

c.close()

