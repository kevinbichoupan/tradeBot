"""
equityDataSetGeneration.py

This script is purposed to generate and populate  a sqlite3 database with all the data for a set of stocks
"""

from databaseInitializeScript import *
from generateFundamentals import *
from generateDailyMarketHistory import *

"""
equities = ['DHI', 'LEN', 'NVR', 'PHM', 'HD', 'LOW', 'SHW', 'BLD', 'TOL', 'MAS', 'KBH', 'TMHC', 'FBHS', 'MHK', 'MTH', 'LGIH', 'MDC', 'LII', 'TREX', 'FND', 'OC', 'BLDR', 'WSO', 'IBP', 'TPH', 'SKY', 'CVCO', 'CCS', 'LPX', 'LEG', 'MHO', 'EXP', 'AZEK', 'UFPI', 'SSD', 'LENB', 'GRBK', 'DOOR', 'BECN', 'BZH', 'JELD', 'AMWD', 'PGTI', 'NX', 'LL', 'ETH', 'XTSLA']
"""

equities = ['SPY', 'QQQ', 'AAPL', 'TSLA', 'MSFT']


portfolioName = '1a_test'



if __name__ == '__main__':
	print('\n\n\n')
	print('==============================================')

	databaseInfo = createPortfolioTables(portfolioName)

	for i in equities:
		print('\n==============================================')	
		print('\n\nBEGIN - Data Load for ' + i)

		print('\nBEGIN - generateFundamentals')
		insertCurrentFundamentalData(i, databaseInfo)
		print('END - generateFundamentals\n')

		print('\nBEGIN - generateDailyHistoricals')
		insertEquityHistory(i, databaseInfo)
		print('END - generateDailyHistoricals\n')

		print('COMPLETE - Data Load for ' + i)	
		print('==============================================\n')

