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

from ib_insync import *


__all__ = [ 'Screeners',
             'BullPutScreener' ]
# add more here

class Screeners():
    def __init__( self  ):
        self.Ib = ib
        self.bullPutScreener = BullPutScreener( ib )

    def setUnderlyingUniverse( self, underlyingUniverse : List[ str ] ):
        """
            args:
                underlyingUniverse : Ticker list of underlying to scan with
                    unrelyingFilterParams. This could be, for example, the
                    entire S&P500 index constituents
        """
        self.underlyingUniverse = underlyingUniverse

    def setUnderlyingScannerParameters( self, filterParams : Dict[ str, float] ):
        """
            provide screening parameter dictionary
            args:
                filterParams: Security filter parameters:
                    min_market_cap =  minimum market capital in USD Millions Dollars
                    constituents_slice =    After minimum market cap ordering /
                                filtering scan up to to this number of securities
                    min_option_volume =   minimum average daily option volume
                    min_iv_rank = min 52 weeks Implied Volatility Rank (%)
                    min_days_to_earnings =  minimum days to next earnings report
        """
        self.underlyingScreenerParams = dict

    def setBullPutSccreenerParameters( self, filterParams : Dict[str,str]  ):
        """
            Set bull put screener parameters
            List of parameters available in 'bullputverticals_scr' file
        """
        self.bullPutScreener.setFilterParameters( filterParams )

    def executeUnderlyingScan( self ):
        logging.info( "Executing underlying scanner" )
        #TODO

    def runBullPutScreener( self ):
        logging.info( "Executing bull put stratery screener" )
        #TODO
