"""
Import all available screeners

author: Sergio Espinoza sergio.espinoza.lopez@gmail.com
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
