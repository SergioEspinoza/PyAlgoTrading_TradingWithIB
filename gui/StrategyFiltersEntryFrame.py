"""
    Frame subclass with labels and text entries for value in variable:
        pass several option strategy screening parameters

    author: Sergio Espinoza
    sergio.espinoza.lopez@gmail.com
"""

import tkinter as tk
from .ParameterTextEntry import ParameterTextEntry
from .StrategyFiltersi import StrategyFilters


class StrategyFiltersEntryFrame( tk.Frame ):

    def __init__( self, container, **kwargs):
        """
        Option strategy filters:
             * pct_under_px_range: .20  scan strikes under this % below market price for underlying
             * num_month_expiries: 3 monthly expires forward
             * max_loss: max loss
             * min_profit: min profit
         """
         super().__init__( container, **kwargs )

        #Percentage under price
        self.pctUnderPxEntry = ParameterTextEntry( self, 'Pct Under Price (0-99%)' )
        self.pctUnderPxEntry.pack( fill='x', expand=True )

        #Number of monthly expiries
        self.monthlyExpiriesEntry = ParameterTextEntry( self, 'Monthly expiries' )
        self.monthlyExpiriesEntry.pack( fill='x', expand=True )

        #Max loss
        self.maxLossEntry = ParameterTextEntry( self, 'Max loss' )
        self.maxLossEntry.pack( fill='x', expand=True )

        #Min Profit
        self.minProfitEntry = ParameterTextEntry( self, 'Min Profit' )
        self.minProfitEntry.pack( fill='x', expand=True )

        #store string variables
        self.pctUnderPxEntryVar = self.pctUnderPxEntry.getParameterStringVar()
        self.monthlyExpiriesEntryVar = self.monthlyExpiriesEntry.getParameterStringVar()
        self.maxLossEntryVar = self.maxLossEntry.getParameterStringVar()
        self.minProfitEntryVar = self.minProfitEntry.getParameterStringVar()

        def getStrategyFilters( self )-> StrategyFilters:
            return StrategyFilters(
                 pct_under_px_range = float(self.pctUnderPxEntryVar.get()),
                 num_month_expiries = int( self.monthlyExpiriesEntryVar.get() ),
                 max_loss = int(self.maxLossEntryVar.get()),
                 min_profit = int( minProfitEntryVar.get())
            )
