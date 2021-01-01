"""

TRADING ALGORITHM - TD Ameritrade API Data Feed Service


"""



# import packages
import requests as requests
from datetime import date
import configparser
import json

# assign alpha vantage key for access

config = configparser.ConfigParser()
config.read('/Users/kevinbichoupan/projects/tradeBot/config.conf')
TDAmeritradeConfigs = dict(config.items('TD Ameritrade API'))



class TDAPIService():

	def __init__(self, TDAPIKey: str = TDAmeritradeConfigs['apikey']):
		self.TDAPIKey = TDAPIKey






	def getCheckMarketOpen(self, market: str):
		market = market.upper()
		marketLC = market.lower()

		getRequestUrl = "https://api.tdameritrade.com/v1/marketdata/" + market + "/hours?apikey=" + self.TDAPIKey
		response = requests.get(getRequestUrl)

		try:
			response.raise_for_status()
		except requests.exceptions.HTTPError as e:
			return "Unsuccessful API Call - getCheckMarketOpen | Error: " + str(e)

		return json.loads(response.text)[marketLC][marketLC]['isOpen']






	def getQuote(self, symbol: str):
		symbol = symbol.upper()
		getRequestUrl = "https://api.tdameritrade.com/v1/marketdata/" + symbol + "/quotes?apikey=" + self.TDAPIKey
		response = requests.get(getRequestUrl)
		
		try:
			response.raise_for_status()
		except requests.exceptions.HTTPError as e:
			return "Unsuccessful API Call - getQuote | Error: " + str(e)
		
		return json.loads(response.text)





	def getFundamentals(self, symbol: str):
		symbol = symbol.upper()
		getRequestUrl = "https://api.tdameritrade.com/v1/instruments?symbol=" + symbol + "&projection=fundamental&apikey=" + self.TDAPIKey
		response = requests.get(getRequestUrl)

		try:
			response.raise_for_status()
		except requests.exceptions.HTTPError as e:
			return "Unsuccessful API Call - getFundamentals | Error: " + str(e)
		
		return json.loads(response.text)





	def getPriceHistory(self, symbol: str, startDate: int, endDate: int):
		symbol = symbol.upper()
		getRequestURL = "https://api.tdameritrade.com/v1/marketdata/" + symbol + "/pricehistory?apikey=" + self.TDAPIKey + "&startDate=" + startDate + "&endDate=" + endDate  + "&periodType=month&frequencyType=daily&frequency=1"
		response = requests.get(getRequestURL)

		try:
			response.raise_for_status()
		except requests.exceptions.HTTPError as e:
			print( "Unsuccessful API Call - getPriceHistory | Error: " + str(e))

		return json.loads(response.text)




"""
	def getMovers(self, indexSymbol, direction, change):
		https://developer.tdameritrade.com/movers/apis/get/marketdata/%7Bindex%7D/movers

	def getPriceHistory(self, symbol: str):
		https://developer.tdameritrade.com/price-history/apis/get/marketdata/%7Bsymbol%7D/pricehistory

	def getAccount(self, AccountID: str):
		https://developer.tdameritrade.com/account-access/apis/get/accounts/%7BaccountId%7D-0

	def getOrder():
		https://developer.tdameritrade.com/account-access/apis/get/accounts/%7BaccountId%7D/orders/%7BorderId%7D-0

	def postPlaceOrder():
		https://developer.tdameritrade.com/account-access/apis/post/accounts/%7BaccountId%7D/orders-0

	def deleteCancelOrder():
		https://developer.tdameritrade.com/account-access/apis/delete/accounts/%7BaccountId%7D/savedorders/%7BsavedOrderId%7D-0

	def getTransactions():
		https://developer.tdameritrade.com/transaction-history/apis/get/accounts/%7BaccountId%7D/transactions-0

	def getTransaction():
		https://developer.tdameritrade.com/transaction-history/apis/get/accounts/%7BaccountId%7D/transactions/%7BtransactionId%7D-0

"""
