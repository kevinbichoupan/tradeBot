"""

TRADING ALGORITHM - Paper Portfolio Tracking Service


"""



# import packages
import pandas as pd
import requests as requests
import datetime
import json
import os



class TradeOrder():

	def __init__(self, enteredTime: str, duration: str, orderType: str, instruction: str, symbol: str, quantity: int, price: float = None, stopPrice: float = None):

		self.enteredTime = enteredTime #datetime of when order was placed
		self.duration = duration # 'DAY' or 'GOOD_TILL_CANCEL' or 'FILL_OR_KILL'
		self.orderType = orderType # 'MARKET' or 'LIMIT' or 'STOP' or 'STOP_LIMIT' or 'TRAILING_STOP' or 'MARKET_ON_CLOSE' or 'EXERCISE' or 'TRAILING_STOP_LIMIT' or 'NET_DEBIT' or 'NET_CREDIT' or 'NET_ZERO'
		self.instruction = instruction # 'BUY' or 'SELL' or 'BUY_TO_COVER' or 'SELL_SHORT' or 'BUY_TO_OPEN' or 'BUY_TO_CLOSE' or 'SELL_TO_OPEN' or 'SELL_TO_CLOSE' or 'EXCHANGE'
		self.symbol = symbol # ticker symbol of instrument for order
		self.quanity = quantity # quantity of instrument for order
		self.price = price # optional argument, order price
		self.stopPrice = stopPrice # optional argument, order stop Price
		self.fulfilled = False # Default to False, will trigger to True if order is fullfilled
		self.fulfilledTime = None # Default to None, Datetime of order fulfillment

	def checkForFulfillment(self, marketData):
		if self.orderType == 'MARKET':
			self.fulfilled = True
			self.fulfilledTime = marketData.datetime
			self.price = marketData.price


class PaperPortfolio():

	def __init__(self, portfolioName: str, initialDeposit: float):
		# Set Class Attributes
		
		self.portfolioName = portfolioName
		self.dirPath = "/Users/kevinbichoupan/Algotrade/Files/Paper Trading Portfolio Files/" + self.portfolioName 
		self.transactionHistoryPath = self.dirPath + "/Transaction_History.csv"
		self.initialDeposit = initialDeposit
		self.openOrders = []
		self.fulfilledOrders = []

		# Check for Paper Portfolio directory and Create if not exists
		
		if not os.path.exists(self.dirPath):
			os.makedirs(self.dirPath)

		# Check for Transaction History File and Create if not exists

		if not os.path.exists(self.transactionHistoryPath):
			initializeTransactionHistoryDict = {
				'transactionID' : 0,
			    'transactionDT' : datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
			    'tranType' : 'Initialize Account',
			    'symbol' : None,
			    'totalAmount' : self.initialDeposit,
			    'unitAmount' : None,
			    'quantity' : None,
			    'portfolioAmountAdj' : self.initialDeposit,
			    'portfolioQuantityAdj' : None
			}
			tmpdf = pd.DataFrame(initializeTransactionHistoryDict, index = [0])
			tmpdf.to_csv(self.transactionHistoryPath, index=False)

		self.transactionHistory = pd.read_csv(self.transactionHistoryPath)

	def refreshOrders(self, marketData):
		tmpUnfulfilledOrders = []
		tmpFulfilledOrders = []
		for i in self.openOrders:
			i.checkForFulfillment(marketData)
			if i.fulfilled:
				tmpFulfilledOrders.append(i)
			else:
				tmpUnfulfilledOrders.append(i)
		self.openOrders = tmpUnfulfilledOrders
		self.fulfilledOrders = tmpFulfilledOrders

	def generateTransactionHistory(self):
		fulfilledOrderDicts = []

		for i in self.fulfilledOrders:
			tmpDict = {
				'transactionDt' : i.fulfilledTime,
				'tranType' : i.orderType + ' - ' + i.instruction,
				'symbol' : i.symbol,
				'totalAmount' : i.price * i.quantity,
				'unitAmount' : i.price,
				'quantity' : i.quantity,
				'portfolioAmountAdj' : i.price * i.quantity if i.instruction == 'BUY' else -i.price * i.quantity if i.instruction == 'SELL' else 'ORDER INSTRUCTION NOT MAPPED',
				'portfolioQuantityAdj' : i.quantity if i.instruction == 'BUY' else -i.quantity if i.instruction == 'SELL' else 'ORDER INSTRUCTION NOT MAPPED',
			}

			fulfilledOrderDicts.append(tmpDict)




	def addTransaction(self, transactionDict):

		transactionData = pd.DataFrame(transactionDict, index=[0])
		transactionData['transactionID'] = self.transactionHistory['transactionID'].max()

		updatedTransactionHistory = pd.concat([self.transactionHistory, transactionData], sort=False)
		updatedTransactionHistory.to_csv(self.transactionHistoryPath, index=False)

		self.transactionHistory = pd.read_csv(self.transactionHistoryPath)








	def portfolioDetails(self):

		currentBalance = self.transactionHistory['portfolioAmountAdj'].sum()
		positions = self.transactionHistory.groupby(['symbol'])['portfolioQuantityAdj'].sum()













