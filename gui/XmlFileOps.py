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


    def loadFromXmlFile( self, filename ) -> bool :
        """
        Parse parameter values xml file and store result
        into instance variables 'securityFilters' and 'strategyFilters'

        return: True if parser success
        """

        logging.info( f'parsing {filename} file' )

        tree = ET.parse( filename )

        root = tree.getroot()

        if( root is not None ):

            logging.info( "root element created" )

            if root.tag == 'BullPutScreener':

                logging.info( 'Loading Bull Put Screener parameters...' )

                securityFilters = SecurityFilters();
                try:
                    securityFilters.loadFromXmlElem( root )
                except Exception as e:
                    logging.error( f"{e}" )

                self.securityFilters = securityFilters

                strategyFilters = StrategyFilters()
                try:
                    strategyFilters.loadFromXmlElem( root )
                except Exception as e:
                    logging.error( f"{e}" )

                self.strategyFilters = strategyFilters

            else:
                logging.info( 'Cannot find BullPutScreener tag!' )

        else:
            logging.error( f'unable to parse {filename} file' )



    def saveToXmlFile( self, filename ):
        """
            arguments:
                filename: xml file output name
            Save current bull put screener settings into xml format
            file format:
            <?xml version="1.0" encoding="UTF-8"?>
                < BullPutScreener >

                    < parameter >
                        <name>"parameter1Name"</name>
                        <value>float</value>
                    < /parameter >

                    < parameter >
                        < name>
                    < /parameter >
                < /BullPutScreener >
                    ...
        """
        # self.minMarketCap = minMarketCap,
        # self.constituentsSlice = constituentsSlice ,
        # self.minOptionVolume = minOptionVolume,
        # self.minIvRank = minIvRank,
        # self.minDaysToEarnigns = minDaysToEarnigns



        # self.pctUnderPxRange = pctUnderPxRange
        # self.numMonthlyExpiries = numMonthlyExpiries
        # self.maxLoss = maxLoss
        # self.minProfit = minProfit

        #TODO
        pass




if __name__ == '__main__':
    print( 'Invoking unit test for ParameterXMLParser class' )
