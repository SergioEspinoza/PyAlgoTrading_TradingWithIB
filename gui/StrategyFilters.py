'''
Copyright 2020 Sergio Espinoza Lopez sergio.espinoza.lopez@gmail.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the 'Software'), to deal
in the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to
do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

  Convenience data class for holding several option strategy screening
  parameters
'''

from dataclasses import dataclass
from typing import TypeVar, Dict, ClassVar

import xml.etree.ElementTree as ET

from xml.etree.ElementTree import ElementTree, Element

import logging

Element_t = TypeVar( 'Element' )


class StrategyFilters():
    """
        Option strategy filter values
    """

    #short descpription for each stored filter parameter
    shortDesc: ClassVar[ Dict[ str, str ] ] = {
        'pctUnderPx' : 'Limit scan under Px (%)',
        'numMonthlyExpiries' : 'No. mothly expiries',
        'maxLoss' : 'Max loss',
        'minProfit' : 'Min Profit'
    }


    # storing tool tips on parameter entries

    toolTips : ClassVar[ Dict[ str, str ] ] = {
        'pctUnderPx' : 'scan strikes under this % below market price for ' \
                            'underlying',
        'numMonthlyExpiries' : 'number of monthly expires forward to scan',
        'maxLoss' : 'Maximum loss allowed',
        'minProfit' : 'Minimum Profit of the strategy'
    }


    def __init__( self, pctUnderPxRange : float = 20,
                        numMonthlyExpiries : int = 3,
                        maxLoss : float = 2000,
                        minProfit : float = 200 ):
        """
        parameters:

        pctUnderPx:  scan strikes under this % below market price for underlying


        numMonthlyExpiries : number of monthly expires forward to scan
                             (i.e. if today is 1st Aug , then motnhly expiries
                              up to - but not including - November will be
                              scanned ),

        maxLoss: Maximum loss allowed, in a vertical spread strategy
                  (like bull put spread) this should influence maximum allowed
                  distance between strikes,

        minProfit : Minimum Profit of the strategy, case of credit spread
                     this would be the minimum premium value
        """
        self.pctUnderPx = pctUnderPxRange,
        self.numMonthlyExpiries = numMonthlyExpiries,
        self.maxLoss = maxLoss,
        self.minProfit = minProfit


    def loadFromXmlElem( self, elementSubTree : Element_t  ):
        """
        Initialize using xml subtree of 'underlyings' tag

        arguments
            elementSubTree: xml 'element' including the 'strategy'
                            tag and its sub-tree
        """

        strategyEl = elementSubTree.find( 'strategy' )

        if strategyEl is not None:

            parameters = strategyEl.findall( 'parameter' )

            logging.info( f'Parsing strategy group with {len(parameters)}' \
            'parameters' )

            for parameter in parameters:
                nameEl = parameter.find( 'name' )
                valueEl = parameter.find( 'value' )
                try:
                    #set value
                    logging.info( f'setting {nameEl.text} to {valueEl.text}' )
                    setattr( self, nameEl.text, valueEl.text )

                except Exception as e:
                    logging.error( f'{e}' )
        else:
            logging.error( 'Unable to find strategy tag! ' )

    def saveToXmlElem( self, elementSubTree : Element_t ):
        """
            Save to xml tree Element
                arguments
                    elementTree: mpty element sub-tree at which to save parameters.
                             'strategy' and sub-tree will be created
        """
        strategyEl = elementSubTree.Element( 'strategy' )

        for attribute in dir(self):

            value = getattribute( self,  attribute )
            #create new parameter
            parElement = elementSubTree.Element( 'parameter' )

            #name element
            parElement = parElement.Element( 'name' )
            parElement.text = attribute

            #assign value
            valueEl = parElement.subElement( 'value' )
            valueEl.text = value
