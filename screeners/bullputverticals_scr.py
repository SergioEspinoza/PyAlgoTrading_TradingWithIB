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
    def __init__( self, ib: IB = None,
                  constituents: List[ str ] = None,
                  filterParams : Dict[ str, float ] = None,
                   loop = None ):
        """ 
            arguments:
                ib : main Interactive Brokers interface from ib_insync, should be
                     'connected'
                constituents: comma separated file with tickers to scan
               filterParams: Bull Put screener parameters, see 'setFilterParameters'
                             method for available keys
               loop: asyncio event loop for concurrent screener execution

        """

        self.ib = ib
        self.constituentsList = constituents
        self.filterParams = filterParams
        self.loop = loop

    def setFilterParameters( self, filterParams : Dict[ str, str] ):
        """
        #option strategy filters
        args:
            filterParams: strategy filter parameters
                - pct_under_px_range: scan strikes under this % below market price for underlying
                - num_month_expiries: monthly expires forward
                - max_loss:  max loss
                - min_profit: min profit
        """
        self.filterParams = filterParams


    def setConstituentsList( self, constituentsList : List[str] ):
        """
            args:
                constituentsList : list of undrelying tickers to scan
        """
        self.constituentsList = constituentsList

    def executeScan( self, taskNum: int = 1 ):
        """
        Execute bull put screening algorithm.
        Divide work in up to 'taskNum' tasks of concurrent execution

        arguments:
            taskNum: number of task to divide the work among, for now only 1
                     working
        """
        pass

if __name__ == "main":
    logging.info('Runnning bullputvertical_scr test')
