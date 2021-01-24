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

from typing import List, Dict

from ib_insync import *

from datetime import datetime, timedelta

import logging

import xml.etree.ElementTree as ET

__all__ = 'ScreenerUtils'

class ScreenerUtils():

    _ib : IB = None


    def __init__(self):
        pass

    @classmethod
    def getSp500Constituents( cls, filename ):
        """
        get S&P500 constituents via datahub.io Package, store to file
            Args:
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

            Args:
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

            Args:
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

    @classmethod
    def filterByUpcomingEarnings( cls, contractList : List[ Contract ],
    minDaysToEarnigns : int ) -> List[Contract]:
        """
        Filter US 'stock' contracts based on earning report. Query their
        next earning report and filter out based on 'minDaysToEarnigns' parameter.
        (Filter out if earning report happens sooner). Contracts whould be
        qualified already
            Args:
                symbolList : List of symbols to filter
                minDaysToEarnigns : minimum number of days until next earning report
            Return:
                List of filtered contracts
        """

        assert minDaysToEarnigns > 0
        assert minDaysToEarnigns < 90


        filteredContracts = []

        clearEarningsDate = datetime.now() + timedelta( days = minDaysToEarnigns )
        #request fundamental data
        for c in contractList:
            logging.info( f'requesting fundamental data for {c.symbol}' )

            try:
                xmlString = cls._ib.reqFundamentalData( c, 'CalendarReport' )

                xmlroot = ET.fromstring( xmlString )

                for earningNode in xmlroot.iter( 'Earnings' ):
                    dateNode = earningNode.find( 'Date' )
                    earningsDate = pd.to_datetime( dateNode.text )

                    if( earningsDate < clearEarningsDate ):
                        filteredContracts.append( c )

            except Exception:
                xmlString = None

        return filteredContracts

    @classmethod
    def reqScannerParameters( cls ) -> List[str]:
        parameters = cls._ib.reqScannerParameters()

        return parameters


    @classmethod
    def twsConnect( cls, host : str = '127.0.0.1', port : int = 7497, client: int = 25 ) -> IB:
        """
        Connect to TWS API via 'IB.connect' method, register disconnection handler
        Args:
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

        cls._ib.RaiseRequestErrors = False

        return cls._ib


    @classmethod
    def reqOptionChains( cls, contracts : List[ Contract ],
                              pct_px_range : int,
                              num_month_expiries : int ) -> Dict[ str, List[ OptionChain ] ]:
        """
        Request option chains for underlyings in contract list.
        Option chains will be filtered out if exchange is not 'SMART' as well as  strike /
        expiration combinations based on function arguments.
        Args:
            contracts : List of contracts to request options chains for.
            pct_px_range : maximum allowed strike variation (%) around current market price
            num_month_expiries : maximum number of monthly expiries to look for (in the future).
                                 weekly expirations earlier than last month will be included.
        Returns: { symbol : 'List[OptionChain]' } where 'List' are the option chains for 'symbol',
         strikes and expirations filtered based on provided arguments.
         Option chain object memebers defined (as in ib_insync):
            exchange: option chains belonging to 'SMART' exchange only
            underlyingConId: underlying contract
            tradingClass: the option trading class
            multiplier: the option multiplier
            expirations : filtered out according to 'num_month_expiries'
            strikes : filtered out according to 'pct_px_range'
        """

        #get unfiltered chains
        chains = { c.symbol : cls._ib.reqSecDefOptParams( c.symbol, '', c.secType, c.conId ) for c in contracts  }

        #leave only 'SMART' exchange chains (should be one per contract)
        chains = { symbol : [ c for c in chainList if c.exchange == 'SMART'  ] for ( symbol, chainList )  in chains.items() }
        chains = { s : c[0] for ( s, c ) in chains.items() }

        #prepare datetime for expiration filtering
        curdate = datetime.now()
        delta_forward = timedelta( weeks = num_month_expiries*4 )
        option_expiration_limit = curdate + delta_forward

        #get tickers
        tickers = cls._ib.reqTickers( *contracts )

        logging.info( f"Retrieved {len(tickers)} contract tickers (snapshot)" )

        tickerDict = { t.contract.symbol : t for t in tickers }

        adjustedChains = {}
        #filter strikes by pct_px_range and expirations by num_month_expiries
        for ( symbol, chain ) in chains.items():

            curPrice = tickerDict[symbol].marketPrice()

            newstrikes = [ s for s in chain.strikes if s >= ( curPrice * ( 1 - ( pct_px_range / 100 ) ) ) and s <= ( curPrice * ( 1 + ( pct_px_range / 100 )  ) ) ]

            newexpirations = [ e for e in chain.expirations if pd.to_datetime(e) < option_expiration_limit ]

            #OptionChain is 'NamedTuple' (not mutable)
            adjustedChain = OptionChain( chain.exchange,
                                    chain.underlyingConId,
                                    chain.tradingClass,
                                    chain.multiplier,
                                    newexpirations,
                                    newstrikes )

            adjustedChains.update( { symbol : adjustedChain } )

        return adjustedChains



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
