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

    Should be able to provide concurrent execution of the main algorithm
    while being able to configure the number of concurrent tasks.

"""

from ib_insync import *

import asyncio

from typing import List, Mapping, TypeVar, Dict, Type

import pandas as pd

import logging


class BullPutScreener( ):

    """
        These parameters are also shared with other strategies.
        No other parameters defined so far
    """
    _bullPutStrategyScreenerAvailParameters = [
        'pct_px_range',
        'num_month_expiries',
        'max_loss',
        'min_profit'
    ]


    def __init__( self, ib: IB = None,
                  underlyingContracts: List[ str ] = None,
                  strategyScannerParams : Dict[ str, float ] = None,
                   loop = None ):
        """ 
            arguments:
                ib : main Interactive Brokers interface from ib_insync, should be
                     'connected'
                constituents: comma separated file with tickers to scan
               strategyFilterParams: Bull Put screener parameters, see 'setFilterParameters'
                             method for available keys
               loop: asyncio event loop for concurrent screener execution

        """

        self.ib = ib
        self._underlyingContracts = underlyingContracts
        self._scannerParams = strategyScannerParams
        self.loop = loop

    def setScannerParameters( self, scannerParams : Dict[ str, str] ):
        """
        #option strategy filters
        args:
            filterParams: strategy filter parameters
                - pct_under_px_range: scan strikes under this % below market price for underlying
                - num_month_expiries: monthly expires forward
                - max_loss:  max loss
                - min_profit: min profit
        """

        for (key,value) in self._scannerParams.items():
            if value not in self._bullPutStrategyScreenerAvailParameters:
                logging.warning( f'{key} parameter not avilable for bull put screener' )

        self._scannerParams = scannerParams


    def setUnderlyingContracts( self, underlyingContracts : List[Contract] ):
        """
            args:
                constituentsList : list of undrelying tickers to scan
        """

        self._underlyingContracts = constituentsList

    def execute( self, taskNum: int = 1 ) -> List[Contract]:
        """
        Execute bull put screening algorithm.
        Divide work in up to 'taskNum' tasks of concurrent execution

        arguments:
            taskNum: number of task to divide the work among, for now only 1
                     working

        returns:
            list of 'combo' contracts that match the criteria
        """
        logging.info( "bull put screener execution start!" )

        # screened contracts will be placed here, one list per contract
        # { symbol : [ { expiration : dataframe }, ... ] }
        combosByContract = {}
        combosByChain = {}


        # Create / Filter combos
        for ( symbol, contract ) in self._underlyingContracts.items():

            #make sure within liquid hours
            # if( withinLiquidHours( symbol ) == False ):
            #     print('market closed for {}'.format(symbol))
            #     continue


            #TODO: make below code work
            for chain in adjustedContractChains[ symbol ]:

                # ----- expirations loop -----
                for exp in chain.expirations:

                    # results per expiration
                    results = []

                    #create contracts for all strikes
                    comboContracts = [Option(symbol, exp, strike, 'P', contract.exchange )
                            for strike in chain.strikes]

                    comboContracts = ib.qualifyContracts( *comboContracts )

                    # might need to be less than 100 requests (IB limit depending on data subscription)
                    comboTickers = ib.reqTickers( *comboContracts )

                    print( '{} tickers received for expiration {} in contract chain'.format( len(comboTickers), exp, symbol ) )

                    # ---- leg1 loop ----
                    for leg1Ticker in comboTickers:
                        leg1Price = leg1Ticker.marketPrice()
                        leg1Strike = leg1Ticker.contract.strike
                         # early filter leg1 by min_profit
                        if( ( leg1Price * int(chain.multiplier) ) < min_profit ):
                            comboContracts.remove(leg1Ticker.contract)
                        else:
                            #fix leg 1
                            leg1 = ComboLeg(conId=leg1Ticker.contract.conId,
                                            ratio= 1,
                                            action='SELL',
                                            exchange=leg1Ticker.contract.exchange )
                            # ---- leg 2 loop ----
                            for leg2Ticker in comboTickers:
                                leg2Strike = leg2Ticker.contract.strike
                                if( leg2Ticker.contract.strike < leg1Strike ):
                                    leg2Price = leg2Ticker.marketPrice()
                                    #leg2 hedge should cost less than leg1
                                    comboPrice = ( leg1Price - leg2Price ) * int(chain.multiplier)

                                    if ( comboPrice < max_loss ) and \
                                    ( comboPrice > min_profit ):

                                        leg2 = ComboLeg( conId=leg2Ticker.contract.conId,
                                                        ratio=1,
                                                        action='BUY',
                                                        exchange=leg2Ticker.contract.exchange )

                                        #create 'combo contract'
                                        combo = Contract( symbol=leg1Ticker.contract.symbol,#check!!
                                                         secType='BAG',
                                                         currency='USD',
                                                         exchange=leg1Ticker.contract.exchange,
                                                         comboLegs=[leg1, leg2])

                                        #market price only during market hours
                                        order = MarketOrder( action="BUY",
                                                           totalQuantity = 1 )

                                        #this method is blocking
                                        orderState = ib.whatIfOrder( combo, order )

                                        roc = comboPrice / float(orderState.maintMarginChange)

                                        #model greeks might not be pupulated (check)
                                        if leg1Ticker.modelGreeks != None :
                                            leg1IV = leg1Ticker.modelGreeks.impliedVol
                                            leg2IV = leg2Ticker.modelGreeks.impliedVol
                                        else:
                                            leg1IV = float('nan')
                                            leg2IV = float('nan')


                                        results.append( [ leg1Strike,
                                                           leg1Ticker.contract.conId,
                                                           leg1IV,
                                                           leg2Strike,
                                                           leg2Ticker.contract.conId,
                                                           leg2IV,
                                                           comboPrice,
                                                           float(orderState.maintMarginChange),
                                                           roc ] )


                    combos_df = pd.DataFrame( data = results, columns=[ 'leg1Strike',
                                                                        'leg1ContractId',
                                                                        'leg1IV',
                                                                        'leg2Strike',
                                                                        'leg2ContractId',
                                                                        'leg2IV',
                                                                        'maxProfit',
                                                                        'margin',
                                                                        'ROC' ] )

                    print( '{} combos found for {} contract chain with expiration {}'.format( \
                        len( combos_df.index ), symbol, exp ) )

                    combosByChain.update( { exp : combos_df } )

            combosByContract.update( { symbol : combosByChain } )






if __name__ == "main":
    logging.info('Runnning bullputvertical_scr test')
