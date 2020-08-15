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


    Helper methods for xml parameter file  load / save

"""

from SecurityFilters import SecurityFilters
from  StrategyFilters import StrategyFilters

import xml.etree.ElementTree as ET

import logging

class ParameterXMLParser():

    def __init__( self ):
        self.securityFilters = None
        self.strategyFilters = None

    def parseXmlFile( self, filename ):
        """
        Parse parameter values xml file and store result
        into instance variables 'securityFilters' and 'strategyFilters'
        """

        tree = ET.parse( filename )

        root = tree.getroot()

        #get bull put screen parameters
        for screener in root.findall( 'BullPutScreener' ):

            underlyingFilterParameters = screener.find( 'underlyings' )
            strategyFilterParameters = screener.find( 'strategy ' )


            for parameter in strategyFilterParameters.findall( 'parameter' ):
                if parameter == 'PctUnderPx':
                    pass
                elif parameter == 'NumMonthExpiries':
                    pass
                elif parameter == 'MaxLoss':
                    pass
                elif parameter == 'MinProfit':
                    pass
                else:
                    logging.warning(
                    'xml screener parameter \
                    not recognized'.format( parameter ) )
