"""
    Copyright 2020 Sergio Espinoza Lopez sergio.espinoza.lopez@gmail.com

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights to
    use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
    of the Software, and to permit persons to whom the Software is furnished to
    do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.

    Bull put vertical screening through Interactive Brokers using ib_insync

    Asumes csv file with sp500 constituents tickers and Market Capital
    is available

    Should be able to provide concurrent execution of the main algorithm
    while being able to configure the number of concurrent tasks.

"""

from ib_insync import *

import asyncio

from typing import List, Mapping, TypeVar, Dict, Type

import pandas as pd

import logging


class BullPutScreener( ):
    def __init__( self, ib: Type[IB],
                  loop: Type[asyncio.loop],
                  underlyingsUniverse: list[int] ):
        """ 
            arguments:
                ib : main Interactive Brokers interface from ib_insync, should be
                     'connected'
                loop: asyncio event loop for concurrent screener execution
                constituentsFile: csv file with constituents with at least 'symbol',
                                  'Market Cap' columns
        """
        if ib is None:
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

    def setScreenerParameters( self ):
        """
        """
        pass

    def loadConstituents( self ):
        """

        """
        pass

    def executeScan( self, taskNum: int = 1 ):
        """
        Execute bull put screening algorithm.
        Divide work in up to 'taskNum' tasks of concurrent execution

        arguments:
            taskNum: number of task to divide the work among
        """
        pass

if __name__ == "main":
    logging.info('Runnning bullputvertical_scr test')
