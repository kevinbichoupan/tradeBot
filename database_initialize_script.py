"""

Trading Algorith - Database Initialize Script

"""



import sqlite3



database_name = 'Algotrade_DB.db'
database = '/Users/kevinbichoupan/Algotrade/Files/' + database_name
conn = sqlite3.connect(database)
c = conn.cursor()
print('Connection to Database Successful')


sql_create_equity_history_daily_table = """
CREATE TABLE IF NOT EXISTS equity_history_daily (
	symbol TEXT
	,date TEXT
	,close REAL
	,high REAL
	,low REAL
	,open REAL
	,volume INT
	,PRIMARY KEY (symbol, date)
);"""

c.execute(sql_create_equity_history_daily_table)
print('Successfuly created table equity_history_daily')

