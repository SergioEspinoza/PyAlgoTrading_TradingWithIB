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


This is a tkinter GUI App designed for screening of financial option trading
strategies.

It uses ib_insync Interactive Brokers API
(https://github.com/erdewit/ib_insync)

Interactive Brokers TWS or IB Gateway alpplication needs to be installed and
appropriate API permissions need to be configured along with relevant market
data subscriptions.

Derivative strategies available so far are:

*Credit put verticals (bull put spreads)

It would be possible to extend to more strategies through add ons (not yet
implemented)

Look for conda environment ib_insync_env.yaml file for environment
pre-requisites
"""

from ib_insync import *

import tkinter as tk

from tkinter import ttk

from SecurityFiltersEntryFrame import SecurityFiltersEntryFrame

from StrategyFiltersEntryFrame import StrategyFiltersEntryFrame

from MainMenu import MainMenu

from XmlFileOps import ParameterXMLParser

from typing import TypeVar

from ParameterTextEntry import ParameterTextEntry

import logging

SecurityFilters = TypeVar( 'SecurityFilters' )
StrategyFilters = TypeVar( 'StrategyFilters' )


class MainWindow( tk.Tk ):

    def __init__( self, *args, **kargs ):
        super().__init__( *args, **kargs )
        """
            Create user input area, consists of:

            *'Connect / Disconnect Button'

            *SecurityFiltersEntryFrame (for stage 1 filtering)
                -Run Stage 1 Button

            *StrategyFiltersEntryFrame ( for stage 2 filtering)
                -Run Stage 2 Buttons

            * 'Run' Button
            * 'Status Label' ( Connected / Disconnected )
        """

        parameterParser = ParameterXMLParser()
        #initial parameters from local file
        parameterParser.loadFromXmlFile( './default.xml' )


        self.securityFilters = parameterParser.securityFilters
        self.securitiesEntryFrame = SecurityFiltersEntryFrame( self,
                                    parameterParser.securityFilters )

        self.securitiesEntryFrame.pack( side = 'top' )

        #separator
        ttk.Separator( self, orient='horizontal' ).pack( fill='x',  pady = (10,10) )


        self.strategyFilters = parameterParser.strategyFilters
        self.strategiesEntryFrame = StrategyFiltersEntryFrame( self,
                                    parameterParser.strategyFilters  )

        self.strategiesEntryFrame.pack( side = 'top' )

        ttk.Separator( self, orient='horizontal' ).pack( fill='x',  pady = (10,10) )

        parameterEntry = ParameterTextEntry( self, 'Workers', 'Workers' )
        parameterEntry.pack( side='top' )

        ttk.Separator( self, orient='horizontal' ).pack( fill='x',  pady = (10,10) )

        connectButton = ttk.Button( self, text = 'Connect to TWS', command = self.connectButtonCallback )
        connectButton.pack( side = 'top' )

        ttk.Separator( self, orient='horizontal' ).pack( fill='x',  pady = (10,10) )

        runButton = ttk.Button( self, text = 'Run Underlying Scanner',
                                command = self.runButtonCallback,
                                state = tk.DISABLED )
        runButton.pack( side = 'top' )

        ttk.Separator( self, orient='horizontal' ).pack( fill='x',  pady = (10,10) )

        runButton = ttk.Button( self,
                                text = 'Run Strategy Scanner',
                                command = self.runButtonCallback,
                                state = tk.DISABLED )

        runButton.pack( side = 'top' )

        #TODO: add Status Label (Connected / Disconnected / Error etc)

        self.config( menu = MainMenu( self ) )

    def runButtonCallback( self ):
        logging.info( 'Run Button clicked' )

    def connectButtonCallback( self ):
        logging.info( 'Connect Button clicked' )



def setFilterValues( securityFilters : SecurityFilters ,
                    strategyFilters : StrategyFilters ):
    """
    update entry fields with new filter values
    """
    self.securityFilters = securityFilters
    self.securityFilters = securityFilters

    self.setSecurityFilters


if __name__ == "__main__":
    """
    Test main window creation
    """
    logging.basicConfig(level=logging.INFO)

    window = MainWindow()

    #resize implementation pending
    window.resizable( False, False )

    window.geometry( '400x500' )

    window.mainloop()
