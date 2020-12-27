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

    Import all available screeners
"""

from typing import Dict, List

from .bullputverticals_scr import BullPutScreener
from .utils import ScreenerUtils

import logging

from ib_insync import *


__all__ = [ 'Screeners',
             'BullPutScreener' ]
# add more here

class Screeners():

    "Available underlying screening parameters, to apply on "
    _underlyingScreenerAvailParameters = [
        'min_market_cap',
        'constituents_slice',
        'min_option_volume',
        'min_iv_rank',
        'min_days_to_earnings'
    ]


    _underlyings = []

    def __init__( self, ib : IB ):
        self._Ib = ib
        self.underlyingScreenerParams = None
        #self.bullPutScreener = BullPutScreener( ib )

    @classmethod
    def setUnderlyings( cls, underlyings : List[ str ] ):
        """
            args:
                underlyings : Ticker list of underlying to scan with
                    unrelyingFilterParams. This could be, for example, the
                    entire S&P500 index constituents
        """
        cls.underlyings = underlyings

    def setUnderlyingScannerParameters( self, filterParams : Dict[ str, float] ):
        """
            provide screening parameter dictionary
            args:
                filterParams: Security filter parameters:
                    {'min_market_cap' : float }    minimum market capital in USD Millions Dollars
                    { 'min_option_volume' : float }    minimum average daily option volume
                    { 'min_iv_rank' : float }  min 52 weeks Implied Volatility Rank (%)
                    { 'min_days_to_earnings' : float }  minimum days to next earnings report
                    { 'constituents_slice' : float }  cap number of securities to scan after all other
                                                     filters have been run
        """
        for (key, value) in filterParams.items():
            if key not in self._underlyingScreenerAvailParameters:
                assert False, f'underlying screener key {key} not supported!!!'

        self.underlyingScreenerParams = filterParams

    def setBullPutScreenerParameters( self, filterParams : Dict[str,str]  ) -> List[str]:
        """
            Set bull put screener parameters
            List of parameters available in 'bullputverticals_scr' file
        """
        self.bullPutScreener.setFilterParameters( filterParams )

    def executeUnderlyingScan( self ) -> List[Contract]:

        logging.info( "** Executing underlying scan **" )

        try:
            minMarketCap = self.underlyingScreenerParams[ 'min_market_cap' ]
            minAvgOptionVolume = self.underlyingScreenerParams[ 'min_option_volume' ]
            minIvRank = self.underlyingScreenerParams[ 'min_iv_rank' ]
            minDaysToEarnigns = self.underlyingScreenerParams[ 'min_days_to_earnings' ]

            logging.info( f'First screening criteria: ' )
            logging.info( f'Minimum market capital: {minMarketCap} ' )
            logging.info( f'Minimum Avg Option Vol: {minMarketCap} ' )
            logging.info( f'Minimum IV rank: {minMarketCap} ' )


        except KeyError:
            logging.error( 'Missing scanner parameter' )

        try:
            # use IV rank scan / filter
            symbolList = ScreenerUtils.scanHighIvRankUnderlyings( minMarketCap,
            minAvgOptionVolume,
            minIvRank )

        except Exception as e:
            logging.error( e )

        #build / qualify contracts
        contracts = [ Stock( s, 'SMART' , currency='USD' ) for s in symbolList ]

        qualifiedContracts = self._Ib.qualifyContracts( *contracts )

        assert len(qualifiedContracts) == len(contracts), 'unable to qualify all contracts'

        logging.info(f'{len(qualifiedContracts)} contracts qualify first screening criteria' )
        # filter out 'min_days_to_earnings',
        # 'Wall Street Horizon' subscription needed

        logging.info( f'Next screening criteria:' )
        logging.info( f'Minimum days to next earning report : {minDaysToEarnigns} ' )

        contractList = ScreenerUtils.filterByUpcomingEarnings( qualifiedContracts, minDaysToEarnigns )

        if 'constituents_slice' in self.underlyingScreenerParams.keys():
            slice = int( self.underlyingScreenerParams[ 'constituents_slice' ] )
            contractList = contractList[:slice]

        return contractList

    def setErrorEventHandler( self, handler ):
        self._Ib.errorEvent += handler

    def runBullPutScreener( self ):
        logging.info( "Executing bull put stratery screener" )
        #TODO
