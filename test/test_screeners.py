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

import os

from ib_insync import *

@pytest.fixture( scope='module')
def fixture():
    logging.info( 'test fixture pre' )

    global utils

    #instance might not be used since it declares mostly
    #class methods
    utils = ScreenerUtils()


    yield
    logging.info( 'test fixture post')

@pytest.mark.Utils
@pytest.mark.Utils1
def test_Utils_GetSp500Constituents(fixture):
    logging.info('testing S&P 500 constituent list getter')
    filename= input('enter s&p500 csv filename: ')

    filename='output/'+filename
    logging.info( F'saving to {filename}' )

    ScreenerUtils.getSp500Constituents(filename)

    assert os.path.exists( filename )

    assert ( os.path.getsize( filename ) > 0 )


@pytest.mark.Utils
@pytest.mark.Utils2
def test_Utils_TwsConnect(fixture):
    logging.info( 'testing tes conenct method' )
    #TODO

@pytest.mark.Screener
def test_Screener(fixture):
    logging.info('unit test screener')



@pytest.mark.BullPutScreener
def test_BullPutScreener(fixture):
    logging.info( 'unit test bull put screener' )
