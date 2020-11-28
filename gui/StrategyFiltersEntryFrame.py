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

    def __init__( self, container,
                strategyFilters : StrategyFilters = None, **kwargs):
        """
        Option strategy filters:
             * pct_under_px_range: .20  scan strikes under this % below market price for underlying
             * num_month_expiries: 3 monthly expires forward
             * max_loss: max loss
             * min_profit: min profit
         """
        super().__init__( container, **kwargs )

        ttk.Label( self, text='Option Strategy filters', font=("Times", 10, "bold") ).pack( fill='x', pady= ( 10, 10 ) )

        if strategyFilters is None:
            #set default values
            self.m_strategyFilters = StrategyFilters()
        else:
            self.m_strategyFilters = strategyFilters

        self.m_parameterEntryList = []

        for ( name, shortDesc ) in StrategyFilters.shortDesc.items():
            parameterEntry = ParameterTextEntry( self, name, shortDesc )
            parameterEntry.pack( fill='x', expand=True )
            self.m_parameterEntryList.append( parameterEntry )

        self._updateEntriesFromFilterValues( )



    def _updateFilterValuesFromEntries( self ):
        """
            Update m_securityFilter member with parameter entry values
        """
        for entry in self.m_parameterEntryList:
            value = entry.getParameterStringVar().get()
            name = entry.m_paramName
            setattr( self.m_strategyFilters, name, value )

    def _updateEntriesFromFilterValues( self ):
        for entry in self.m_parameterEntryList:
            for ( name, desc ) in self.m_strategyFilters.shortDesc.items():
                if name == entry.m_paramName:
                    filterValue = getattr( self.m_strategyFilters, name )
                    entry.setParameterTexEntry( filterValue )

    def getStrategyFilters( self ) -> StrategyFilters:
        self._updateFilterValuesFromEntries()
        return self.m_strategyFilters

    def setStrategyFilters( self, filters: StrategyFilters ):
        self.m_strategyFilters = filters
        self._updateEntriesFromFilterValues()
