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


Utility functions for session management, security scanning and more
"""

from datapackage import Package
import pandas as pd

from typing import List

from ib_insync import *

import logging



__all__ = 'ScreenerUtils'

class ScreenerUtils():

    _ib : IB = None


    def __init__(self):
        pass

    @classmethod
    def getSp500Constituents( cls, filename ):
        """
        get S&P500 constituents via datahub.io Package, store to file
            args:
                filename : name of csv file (output from datahub.io)

        """
        package = Package('https://datahub.io/core/s-and-p-500-companies-financials/datapackage.json')

        df = None

        for resource in package.resources:
            if resource.descriptor['datahub']['type'] == 'derived/csv' and \
            resource.descriptor['name'] == 'constituents-financials_csv':
                data_sp500 = resource.read( keyed=True)
                logging.info( type(data_sp500) )
                logging.info( data_sp500[:10] )
                df = pd.DataFrame(data=data_sp500)
                logging.info(df.head())
                break

        if df is not None and ( len( df['Symbol'] ) > 0 ):
            logging.info( F'Output to {filename}' )
            df.to_csv(filename)
        else:
            logging.warning( 'Unable to get s&p 500 constituents' )

    @classmethod
    def filterSymbolsFromCsv( cls, filename: str, symbolColName : str,
                        marketCapColumnName : str = None, minMarketCap : float
                        = None  ):
        """
            Get ticker list from csv file, where tickers are in the
            one column and "columnName" with optional market capital information
            in additional column. If minMarketCap is defined, filter by
            market capital, marketCapColumnName argument needs to be provided

            args:
                filename : csv filename, at least one column should have
                        symbol names
                symbolColumnName: ticker column name
                marketCapColumnName: Name of market capital column
                minMarketCap: minimum market capital (needs marketCapColumnName)

        """
        df = pd.read_csv( filename, index_col = symbolColName )

        if marketCapColumnName is not None and minMarketCap is not None:
            df = df.sort_values( by = marketCapColumnName, ascending=False, axis = 0 )
            #filter by market capital
            symbols = [ index for ( index, item )  in df if df.iloc[ 'index', 'Market Cap' ] >= minMarketCap ]

        else:
            #get symbols
            symbols = df[ 'columnName' ].keys()

            return symbols

    @classmethod
    def scanHighIvRankUnderlyings( cls,  minMarketCap : float = None, minAvgOptionVolume : float = None,
                    minIvRank : float = None ) -> List[str]:
        """
            Scan for contracts in the 'SCAN_ivRank52w_ASC' scanner code. Any argument not
            given it will be ignored. Needs at least one parameter.

            args:
                minMarketCap : minimum market capital in USD$ Million
                minAvgOptionVolume : minimum daily average option volume
                minIvRank: minimum iv rank
        """
        sub = ScannerSubscription(
                instrument='STK',
                locationCode='STK.US.MAJOR',
                scanCode = 'SCAN_ivRank52w_DESC',
                marketCapAbove = minMarketCap,
                averageOptionVolumeAbove = minAvgOptionVolume )

        scanList = cls._ib.reqScannerData( sub, scannerSubscriptionFilterOptions = [ TagValue( 'IV_RANK52', '.10' ) ] )

        #scanList = cls._ib.reqScannerData( sub )

        symbolList = [  scanData.contractDetails.contract.symbol for scanData in scanList ]

        return symbolList

        #TODO: look for min 52 week IV rank, in 'reqScannerParameters()'
        # output

    @classmethod
    def reqScannerParameters( cls ) -> List[str]:
        parameters = cls._ib.reqScannerParameters()

        return parameters


    @classmethod
    def twsConnect( cls, host : str = '127.0.0.1', port : int = 7497, client: int = 25 ) -> IB:
        """
        Connect to TWS API via 'IB.connect' method, register disconnection handler
        args:
            ip : IB gateway IP Address
            port: connection tcp port
            client: client number / id

        returns IB object (from IB API)
        """
        logging.info( 'Utils.twsConnect() method has been invoked' )
        if( cls._ib is None ):
          cls._ib = IB( )

        cls._ib.connectedEvent += cls.onIbConnected
        cls._ib.disconnectedEvent += cls.onIbDisconnected

        cls._ib.connect( host, port, client,readonly=True )

        return cls._ib

    @classmethod
    def twsDisconnect( cls ):
        cls._ib.disconnect()

    @classmethod
    def onIbConnected( cls ):
        logging.info( 'IB connected!' )

    @classmethod
    def onIbDisconnected( cls ):
        logging.warn( 'IB disconnected!' )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    #for more tests look into test_screeners.py module in 'test' direcotry

    print('**** Utils class unit test ****')

    print( 'getSp500Constituents' )

    myinput = input( 'input filename ---> ' )

    print( 'Processing...' )

    Utils.getSp500Constituents( myinput )

    print( 'test twsConnect method')

    ib = Utils.twsConnect()

    print( f'{ib}' )
