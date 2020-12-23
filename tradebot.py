from packages.Paper_Portfolio_Tracking_Service import *
from packages.TD_Ameritrade_Data_Feed_Service import *

"""
# Initialize

Gondi = PaperPortfolio('Gondi', 10000)

i did it!
TDAPIService.getPriceHistory('MSFT')
"""

TDAPIService = TDAPIService()
TDAPIService.getPriceHistory('MJ')

