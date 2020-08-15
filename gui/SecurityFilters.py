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


  Convenience data class for holding several security screening

"""

from dataclasses import dataclass
from typing import ClassVar

from typing import Dict

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree

@dataclass
class SecurityFilters:

    #store parameter values here
    values: Dict[ str, float ] = {
        #minimum market capital in USD Millions Dollars
        "min_market_cap" : 10.0,
        # After minimum market cap ordering
        # and filtering scan up to to this number of securities.
        # Manly used for testing purposes
        "constituents_slice" : 11,
        #minimum average daily option volume
        "min_option_volume" : 10,
        #52 weeks Implied Volatility Rank (%)
        "min_iv_rank" : 10,
        #minimum days to next earnings report
        "min_days_to_earnings" : 25
        }

    # storing tool tips on parameter entries
    toolTips : Dict[ str, str ] = {
        "min_market_cap" : "Minimum market capital in USDM$",

        "constituents_slice" : "Limit scaning to this number \
                                of securities after ordering \
                                top to bottom by market cap",

        "min_option_volume" : "Minimum average daily option \
                               volume",

        "min_iv_rank" : "52 weeks implied volatility rank",

        "min_days_to_earnings" :  "Minimum days to next earnings \
                                   report"
    }

    #associated xml tag for read / write to xml file
    nameToXmlTag: Dict[ str, str ] = {
        "min_market_cap" : "MarketCap",
        "constituents_slice" : "ConstituentsSlice",
        "min_option_volume" : "MinOptionVolume",
        "min_iv_rank" : "MinIVRank",
        "min_days_to_earnings" : "MinDaysToEarnings"
    }



    def __init__( self, element : TypeVar[ElementTree]  ):
        """
            Initialize using xml subtree of 'underlyings' tag
        """
        #invert ditc to find parameter name via pxml tag as key
        xmlToName = { value : key for ( key, value ) in nameToXmlTag.items() }

        for parameter in underlyingFilterParameters.findall ( 'parameter' ):
            xmlTagName = parameter.find( 'name' )
            xmlVallue = parameter.find( 'value' )
        try:
            #set value
            parameterKey = xmlToName[ xmlTagName ]
            values[ parameterKey ] = xmlValue
        except KeyError:
            logging.error( 'parameter not found, unable to load values from  \
                            xml' )
