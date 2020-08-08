
"""
    Frame subclass with labels and text entries for several security
    screening parameters

    author: Sergio Espinoza
    sergio.espinoza.lopez@gmail.com

"""

import tkinter as tk
from .SecurityFilters import SecurityFilters


class FilterParametersFrame( ttk.Frame ):
    """
    'Screner parameter section with screener parameter entries:
            * min_market_cap: minimum market capital in USD Millions Dollars
            * constituents_slice: After minimum market cap ordering / filtering scan up to to this number of securities
            * min_option_volume: minimum average daily option volume
            * min_iv_rank: min 52 weeks Implied Volatility Rank (%)
            * min_days_to_earnings: minimum days to next earnings report
    """

    def __init__( self, container, **kargs ):

        super().__init__( container, **kargs )

        #Market Cap
        self.marketCapEntry = ParameterTextEntry( self, 'Min Market Cap ($USD M)' )
        self.marketCapEntry.pack( fill='x', expand=True )

        #constituents slice
        self.constituentSliceEntry = ParameterTextEntry( self, 'Contituents Slice' )
        self.constituentSliceEntry.pack( fill='x', expand=True )

        #Min Option Volume
        self.minOptionsVolumeEntry = ParameterTextEntry( self, 'Min Option Volume' )
        self.minOptionsVolumeEntry.pack( fill='x', expand=True )

        #Minimum IV
        self.minIVrankEntry = ParameterTextEntry( self, 'Min IV rank' )
        self.minIVrankEntry.pack( fill='x', expand=True )

        #Minimum days to earnings
        self.minDaysToEarningsEntry = ParameterTextEntry( self, 'Min days to earnings' )
        self.minDaysToEarningsEntry.pack( fill='x', expand=True )

        #get entry variables
        self.marketCapEntryVar = self.marketCapEntry.getParameterStringVar()
        self.constituentSliceVar = self.constituentSliceEntry.getParameterStringVar()
        self.minOptionsVolumeVar =  self.minOptionsVolumeEntry.getParameterStringVar()
        self.minIVrankVar = self.minIVrankEntry.getParameterStringVar()
        self.minDaysToEarningsVar = self.minDaysToEarningsEntry.getParameterStringVar()

        def getSecurityFilters( self ) -> SecurityFilters:
            return SecurityFilters(
                min_market_cap = self.marketCapEntryVar.get(),
                constituents_slice = self.constituentSliceVar.get(),
                min_option_volume = self.minOptionsVolumeVar.get(),
                min_iv_rank = self.minIVrankVar.get(),
                min_days_to_earnings = self.minDaysToEarningsVar.get()
            )
