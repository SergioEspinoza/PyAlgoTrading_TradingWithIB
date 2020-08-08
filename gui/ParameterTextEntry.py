"""
Text entry widget with label and entry for text

author: Sergio Espinoza
sergio.espinoza.lopez@gmail.com
"""

import tkinter as tk
from tkinter import ttk



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

    def getParameterStringVar( self ) -> tk.StringVar:
        return self.stringEntryVar
