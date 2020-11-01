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


Convenience class.
Text entry widget with label and entry.

"""

import tkinter as tk
from tkinter import ttk



class ParameterTextEntry( ttk.Frame ):
    """
        Class constitutes screener parameter text entry with label,
        result will be stored in 'entryVar' instance variable
    """
    def __init__( self, container, name : str, label : str, **kwargs ):
        """
            arguments:
                container: parent
                label: text entry description
        """
        super().__init__( container, **kwargs )

        self._stringEntryVar = tk.StringVar()

        label = ttk.Label( self, text=label )
        label.pack( side = 'left', padx = ( 0, 5) )
        self.m_label = label;

        entry = ttk.Entry( self, textvariable = self._stringEntryVar )
        entry.pack( side = 'left', padx = ( 5, 0), fill='x', expand=True )
        self.m_entry = entry

        self.m_paramName = name

    def getParameterStringVar( self ) -> tk.StringVar:
        return self._stringEntryVar

    def setParameterTexEntry( self, value : str ):
        self._stringEntryVar.set( value )
