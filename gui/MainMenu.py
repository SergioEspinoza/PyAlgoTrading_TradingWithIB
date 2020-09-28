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


    Main menu for option strategy screener application

"""

import tkinter as tk
from tkinter import filedialog
import logging

import xml.etree.ElementTree as ET


class MainMenu( tk.Menu ):

    def __init__( self, container, **kwargs ):
        super().__init__( container, tearoff= 0, **kwargs )

        self.screenerApp = container

        fileMenu = tk.Menu( self, tearoff = 0 )


        fileMenu.add_command( label='Load screener..',
                              command=self.showLoadScreenerDialog )

        fileMenu.add_command( label='Save screener...',
                                command=self.showSaveScreenerDialog )

        super().add_cascade( menu=fileMenu, label="File" )

    def showSaveScreenerDialog( self ):
        filedialog.asksaveasfilename( filetypes=[( "XML", "*.xml" )] )


    def showLoadScreenerDialog( self ):
        filename = filedialog.askopenfilename( filetypes=[( "XML", "*.xml" )] )
        print( "load xml file {}".format( filename ) )

        loadScreener( filename )


    def loadScreenerFile( self, filename ):
        """
            load screener parameters from xml file
        """
        pass

    def saveScreenerFile( self, filename ):
        """
            arguments:
                filename: xml file output name
            Save current bull put screener settings into xml format
            file format:
            <?xml version="1.0" encoding="UTF-8"?>
                < screener >

                    < parameter >
                        <name>"parameter1Name"</name>
                        <value>float</value>
                    < /parameter >

                    < parameter >
                        < name>
                    < /parameter >
                < /screener >
                    ...
            </xml>
        """
        #TODO
        pass
