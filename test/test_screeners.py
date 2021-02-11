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

    Unit Tests for screeners library

    pytest based
"""

import pytest
import logging

from screeners import ScreenerUtils
from screeners import Screeners

import os

from ib_insync import *

@pytest.fixture( scope='module')
def fixture():

    global utils

    logging.info( 'attempting TWS connection' )
    global ib
    ib = ScreenerUtils.twsConnect()
    assert ib.isConnected(), 'Unsuccessfull TWS connection attempt!!!'

    yield
    logging.info( 'disconnecting tws session!!!' )
    ScreenerUtils.twsDisconnect()



@pytest.mark.Utils
@pytest.mark.Utils1
def test_Utils_GetSp500Constituents(fixture):
    logging.info('testing S&P 500 constituent list getter')
    filename= input('enter s&p500 csv filename: ')

    filename='output/'+filename
    logging.info( F'saving to {filename}' )

    ScreenerUtils.getSp500Constituents(filename)

    assert os.path.exists( filename )

    assert os.path.getsize( filename ) > 0


@pytest.mark.Utils
@pytest.mark.Utils2
def test_scanUnderlyings(fixture):

    input( 'ScreenerUtils.scanUnderlyings() test. Enter to send request' )

    underlyings = ScreenerUtils.scanHighIvRankUnderlyings(
        minMarketCap = 5000000000,
        minAvgOptionVolume = 5000,
        minIvRank = 0 )

    assert len( underlyings ) > 0, "unable to find underlyings"

    logging.info( f'scanUnderlyings result : {underlyings}' )

    input( '************ results delivered **************' )

    logging.info( '{underlyings}' )

@pytest.mark.Utils
@pytest.mark.Utils3
def test_reqScannerParameters(fixture):
    input( 'test available scanner parameters. Enter to request' )

    parameters = ScreenerUtils.reqScannerParameters()

    assert len( parameters ) > 0, "error while retreiving available parameters"

    logging.info(  f'***Retrieved parametrs  {len(parameters)} *****' )

    file = open( "./availableParams.xml", 'w+' )

    file.write( f'{parameters}' )

    file.close()



@pytest.mark.Screener
@pytest.mark.Screener1
def test_Screener(fixture):
    logging.info('unit test screener')

    securityFilters = {
        'min_market_cap' : 5000000000,
        'min_option_volume' : 5000,
        'min_iv_rank' : 20,
        'min_days_to_earnings' : 30,
        'constituents_slice' : 20}

    screeners = Screeners( ib )

    screeners.setErrorEventHandler( pyTestIbErrorHandler )

    screeners.setUnderlyingScannerParameters( securityFilters )

    contractList = screeners.executeUnderlyingScan(  )

    assert len(contractList) > 0, 'NO SYMBOLS FOUND!!'

    logging.info( '*** Contracts found *** ' )
    logging.info( f'{contractList}' )

@pytest.mark.Utils
@pytest.mark.Utils4
def test_OptionChainsReq(fixture):
    logging.info('testing option chain request')

    securityFilters = {
        'min_market_cap' : 30000000000,
        'min_option_volume' : 10000,
        'min_iv_rank' : 30,
        'min_days_to_earnings' : 30,
        'constituents_slice' : 20}

    screeners = Screeners( ib )

    screeners.setErrorEventHandler( pyTestIbErrorHandler )

    screeners.setUnderlyingScannerParameters( securityFilters )

    contractList = screeners.executeUnderlyingScan(  )

    logging.info( f'***Retrieved {len(contractList)} contracts after underlying scan***' )

    logging.info( f'***Requesting option chains for {[ c.symbol for c in contractList ]} *** ')

    chains = ScreenerUtils.reqOptionChains( contractList, pct_px_range = 10, num_month_expiries = 3 )

    logging.info( f'*** succesfuly retrieved {len(chains.items())} chains ***' )

    sampleKey =  list(chains.keys())

    logging.info( f'Sample option chain for { sampleKey[0] } : {chains[ sampleKey[0] ] }' )


@pytest.mark.Screener
@pytest.mark.Screener2
def test_BullPutScreener(fixture):
    contractList = []
    comboList = []

    logging.info( 'testgin bull put screener' )


    securityFilters = {
        'min_market_cap' : 30000000000,
        'min_option_volume' : 10000,
        'min_iv_rank' : 30,
        'min_days_to_earnings' : 30,
        'constituents_slice' : 20}

    screeners = Screeners( ib )

    screeners.setErrorEventHandler( pyTestIbErrorHandler )

    screeners.setUnderlyingScannerParameters( securityFilters )

    contractList = screeners.executeUnderlyingScan( )

    logging.info( f"{len(ContractList)} unerlying contracts retreived" )

    comboList = screeners.executeBullPutScan( )

    logging.info( f"screener result with {len(comboList)} combo contracts" )






def pyTestIbErrorHandler(  id : int, errorCode : int, errorMsg : str, c : Contract  ):
    logging.info( '***** ERROR RECEIVED IN PYTEST ERROR HANDLER!!! *****' )
    logging.info( f'id: {id} , errorCode: {errorCode}, errorMsg : {errorMsg}' )

@pytest.mark.BullPutScreener
def test_BullPutScreener(fixture):
    logging.info( 'unit test bull put screener' )
