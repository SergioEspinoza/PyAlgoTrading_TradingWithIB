"""




Bull put vertical screening through Interactive Brokers using ib_insync

Asumes csv file with sp500 constituents tickers and Market Capital
is available

Should be able to provide concurrent execution of the main algorithm
while being able to configure the number of concurrent tasks.

author: Sergio Espinoza sergio.espinoza.lopez@gmail.com
"""

from ib_insync import *

import asyncio

from typing import List, Mapping, TypeVar, Dict

import pandas as pd


class BullPutScreener( ):
    def __init__( self, ib : Type[IB],
                  loop: Type[asyncio.loop],
                  constituentsFile: str ):
    """ 
        arguments:
            ib : main Interactive Brokers interface from ib_insync, should be
                 'connected'
            loop: asyncio event loop for concurrent screener execution
            constituentsFile: csv file with constituents with at least 'symbol',
                              'Market Cap' columns
    """

        if ib.isConnected() == False )
            print('Unable to initialize screener')
        else:
            self.ib = ib
            self.loop = loop
            self.constituentsFile = constituentsFile

    def setScreenerParameters( self, dict : Dict[ str, str] ):
        """
            provide screening parameter dictionary

            arguments:
                dict:
                min_market_cap:  minimum market capital in USD Millions Dollars
                constituents_slice:    After minimum market cap ordering / filtering scan up to to this number of securities
                min_option_volume:   minimum average daily option volume
                min_iv_rank: min 52 weeks Implied Volatility Rank (%)
                min_days_to_earnings:  minimum days to next earnings report

                #option strategy filters
                pct_under_px_range: .20  scan strikes under this % below market price for underlying
                num_month_expiries: 3 monthly expires forward
                max_loss:  max loss
                min_profit: min profit
        """
        self.screenerParams = dict

    def setScreenerParameters():

    def loadConstituents():
        """

        """

    def executeScan( self, taskNum: int = 1 ) -> :
        """
        Execute bull put screening algorithm.
        Divide work in up to 'taskNum' tasks of concurrent execution

        arguments:
            taskNum: number of task to divide the work among
        """
