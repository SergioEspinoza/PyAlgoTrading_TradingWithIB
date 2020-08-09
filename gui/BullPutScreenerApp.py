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

            * 'Run All Button'
            * 'Status Label' ( Connected / Disconnected )
        """

        #self.utils = Utils()
        self.securitiesEntryFrame = SecurityFiltersEntryFrame( self )
        self.securitiesEntryFrame.pack( side = 'top' )

        #separator
        ttk.Separator( self, orient='horizontal' ).pack( fill='x',  pady = (10,10) )
        ttk.Label( self, text='Option Strategy filters' ).pack( fill='x', pady= ( 10, 10 ) )

        self.strategiesEntryFrame = StrategyFiltersEntryFrame( self )
        self.strategiesEntryFrame.pack( side = 'top' )


        self.config( menu = MainMenu( self ) )


if __name__ == "__main__":
    """
    Test main window creation
    """

    window = MainWindow()

    #resize implementation pending
    window.resizable( False, False )

    window.geometry( '400x600' )

    window.mainloop()
