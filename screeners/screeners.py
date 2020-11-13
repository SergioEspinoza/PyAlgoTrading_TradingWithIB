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

from .bullputverticals_scr import BullPutScreener
from typing import Dict


__all__ += BullPutScreener
# add more here

class Screeners():
    def __init__( self, ib ):
        self.Ib = ib

        self.bullPutScreener = BullPutScreener( ib )

    def setBullPutSccreenerParameters( self, params : Dict[str,str]  ):
        """
            Set bull put screener parameters
            List of parameters available in 'bullputverticals_scr' file
        """
        self.bullPutScreener.setScreenerParameters( params )

    def setScreenerConstituents( self, fileName : str ):
        #TODO implement, set constituents filename
        pass

    def runBullPutScreener( self ):
        #TODO implement
        pass
