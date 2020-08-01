"""
This is a tkinter GUI App designed for financial derivative trading
strategies creening using Interactive Brokers API / Data through ib_insync
library

Derivative strategies available so far are:

*Credit put verticals (bull put spreads)

It would be possible to extend to more strategies through add ons

Look for conda environment ib_insync_env.yaml file for environment
pre-requisites

author: Sergio Espinoza sergio.espinoza.lopez@gmail.com
"""

from ib_insync import *

import tkinter as tk

from tkinter import ttk

#from .screeners import *


class MainWindow( tk.Tk ):
    def __init__( self, *args, **kargs ):

        super().__init__( *args, **kargs )

        #self.utils = Utils()
        self.userInputFrame = FilterOptionsFrame( self )
        self.userInputFrame.pack()

        self.config( menu = MainMenu( self ) )


class MainMenu( tk.Menu ):
    def __init__( self, container, **kwargs ):
        super().__init__( container, **kwargs )


        fileMenu = tk.Menu( self, tearoff= 0 )
        fileMenu.add_command( label='Save screener...', command=self.saveScreener )
        fileMenu.add_command( label='Load screener..', commmad=self.loadScreener )




class FilterOptionsFrame( ttk.Frame ):

    def __init__( self, container, **kargs ):
        """
            Create user input area, consists of:

            * 'Screner parameter section with screener parameter entries:
                    * min_market_cap: minimum market capital in USD Millions Dollars
                    * constituents_slice: After minimum market cap ordering / filtering scan up to to this number of securities
                    * min_option_volume: minimum average daily option volume
                    * min_iv_rank: min 52 weeks Implied Volatility Rank (%)
                    * min_days_to_earnings: minimum days to next earnings report

                Option strategy filters:
                     * pct_under_px_range: .20  scan strikes under this % below market price for underlying
                     * num_month_expiries: 3 monthly expires forward
                     * max_loss: max loss
                     * min_profit: min profit

            * 'Run Button'
            * 'Status Label'
        """
        super().__init__( container, **kargs )


        #separator
        ttk.Separator( self, orient='horizontal').pack( fill='x', pady = (10,10) )
        ttk.Label( self, text='Underlying filters' ).pack( fill = 'x', pady = ( 10, 10) )

        #Market Cap
        self.marketCapEntry = ParameterTextEntry( self, 'Min Market Cap ($USD M)' )
        self.marketCapEntry.pack( fill='x', expand=True )

        #constituents slice
        self.constituentSlice = ParameterTextEntry( self, 'Contituents Slice' )
        self.constituentSlice.pack( fill='x', expand=True )

        #Min Option Volume
        self.minOptionsVolume = ParameterTextEntry( self, 'Min Option Volume' )
        self.minOptionsVolume.pack( fill='x', expand=True )

        #Minimum IV
        self.minOptionsVolume = ParameterTextEntry( self, 'Min IV rank' )
        self.minOptionsVolume.pack( fill='x', expand=True )

        #Minimum days to earnings
        self.minOptionsVolume = ParameterTextEntry( self, 'Min days to earnings' )
        self.minOptionsVolume.pack( fill='x', expand=True )


        #separator
        ttk.Separator( self, orient='horizontal' ).pack( fill='x',  pady = (10,10) )
        ttk.Label( self, text='Option Strategy filters' ).pack( fill='x', pady= ( 10, 10 ) )

        #Percentage under price
        self.marketCapEntry = ParameterTextEntry( self, 'Pct Under Price (0-99%)' )
        self.marketCapEntry.pack( fill='x', expand=True )

        #Number of monthly expiries
        self.marketCapEntry = ParameterTextEntry( self, 'Monthly expiries' )
        self.marketCapEntry.pack( fill='x', expand=True )







class ParameterTextEntry( ttk.Frame ):
    """
        Class constitutes screener parameter text entry with label,
        result will be stored in 'entryVar' instance variable
    """
    def __init__( self, container, label, **kwargs ):
        """
            arguments:
                container: parent
                label: text entry description
        """
        super().__init__( container, **kwargs )

        self.entryVar = tk.StringVar()

        label = ttk.Label( self, text=label )
        label.pack( side = 'left', padx = ( 0, 5) )
        entry = ttk.Entry( self, textvariable = self.entryVar )
        entry.pack( side = 'left', padx = ( 5, 0), fill='x', expand=True )


if __name__ == "__main__":
    """
    Test main window creation
    """

    window = MainWindow()

    #resize implementation pending
    window.resizable( False, False )

    window.geometry( '400x600' )

    window.mainloop()
