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

    Frame subclass with labels and text entries for value in variable:
        pass several option strategy screening parameters
"""

import tkinter as tk
from tkinter import ttk
from ParameterTextEntry import ParameterTextEntry
from StrategyFilters import StrategyFilters


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

        ttk.Label( self, text='Option Strategy filters' ).pack( fill='x', pady= ( 10, 10 ) )

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
