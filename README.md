# Tradebot


Purpose
============

Project is a machine learning algorithm that can predict the movement of the stock market.



Data
===========

All data from this project is pulled via the TD Ameritrade API



Scripts and Files
================

*databaseInitializeScript.py*
-------------------------------


Purpose: This script is used to initialize the database and tables used to hold the data in this project.  Data is stored using sqlite3 package

Database Name: tradeBot_DW.db

Tables:

	equity_history_daily_raw -> contains the raw daily stock information pulled from TD Ameritrade API.

Execution: This script is only meant to be run when creating new tables within the database



*generateDailyMarketHistory.py*
---------------------------

Purpose: This script is used to generate and update the historical data in the table tradeBot_DW.equity_history_daily_raw.  Current configuration will load data from 2018-01-01 to currentDay - 1

Execution: command line execution as follows:

	--> python generateDailyMarketHistory.py <symbol>



*tdAmeritradeAPIService.py*
---------------------------

Purpose: This script contains a class TDAPIService, which contains all functions used to interface with the TD Ameritrade API.

Usage:

	Import this script into another file using 'from tdAmeritradeAPIService.py import *'
	Initialize the TDAPIService class
	Call the API service functions needed in the script





