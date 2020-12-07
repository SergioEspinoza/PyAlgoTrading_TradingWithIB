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


Utility functions
"""

from datapackage import Package
import pandas as pd

from ib_insync import *

import logging


__all__ = 'ScreenerUtils'

class ScreenerUtils():
    def __init__(self):
        pass

    @classmethod
    def getSp500Constituents( cls, filename ):
        """
        get S&P500 constituents via datahub.io Package
            args: filename

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
    def twsConnect( cls, ip : str = '127.0.0.1', port : int = 7497, client: int = 25
      ) -> IB:
      """
        args:
            ip : IB gateway IP Address
            port: connection tcp port
            client: client number / id
      """
      logging.info( 'Utils.twsConnect() method has been invoked' )



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
