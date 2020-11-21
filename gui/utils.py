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


  IB connection management, should be able to
  notify disconnections / reconnections through
  pop-up windows and handle connections / reconnections
  to TWS gateway
"""
from dataclasses import dataclass
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ib_insync import *
from datetime import date
import asyncio

import logging

@dataclass
class Utils( ):

    #timeout (seconds)
    timeout = 5
    host = "127.0.0.1"
    port = 7497


    def __init__( self, asyncioloop = None,  client: int = 1, rootApp = None   ):
        """
            Args:
                asyncioloop : asyncio event loop to be used for  asynchronous
                              ib_insync calls. 'asyncio.get_event_loop()' gives
                              current loop'. asyncio must support mutiple nested
                              event loops (need ib_insync.util.patchAsyncio() )
                client: IB gateway client number. Round integer. Neded by TWS API to
                        identify request coming from same endpoint.
                rootApp: root application window instance. Additional dialogs will
                         be built upon it
        """
        self.Ib = None
        self.clientId = client
        self.connected = False
        self.rootApp = rootApp
        self.loop = asyncioloop

        rootApp.protocol( 'WM_DELETE_WINDOW', self._onDeleteWindow )



    def _onDisconnected( self ):
        logging.info( 'TWS connection timeout!' )
        self.connected = False

        if self.rootApp != None:
            messagebox.showinfo( title = "Connection Timeout",
                                 message = "Client Disconnected!",
                                 parent = self.rootApp )

    def _onConnected( self ):
        self.connected = True
        self.progressDialog.destroy()

        if self.rootApp != None:
            messagebox.showinfo( title = "Connected!!",
                                 message = f"Connected w/ client ID !!",
                                 parent=self.rootApp )

    def TwsConnect( self, readOnly: bool = False ) -> bool:
        """
            Connect to IB TWS of IB gateway.
            Spawn progress dialog and notify in case of connection success

            Args:

                readOnly: Accces read only mode
                rootApp: Root frame for dialog box notification

            Return:
                True if connection success
        """

        if  self.Ib == None:
            logging.info( 'Creating IB object' )
            self.Ib = IB()
            self.Ib.disconnectedEvent += self._onDisconnected
            self.Ib.connectedEvent += self._onConnected


        if self.Ib.isConnected() == False:

            self.progressDialog = tk.Toplevel( self.rootApp )
            progress = ttk.Progressbar( self.progressDialog, mode='indeterminate' )
            progress.place( x=30, y=60, width=200 )
            progress.pack()
            progress.start()

            try:

                util.run( self.Ib.connectAsync( self.host,
                                 self.port,
                                 self.clientId,
                                 timeout = self.timeout,
                                 readonly = True ) )
            except TimeoutError:
                self._onDisconnected()

            except ConnectionRefusedError:
                self._onDisconnected()


        elif rootApp != None:
            messagebox.showinfo( "Already connected", parent=rootApp )

    def _onGuiUpdateTimeout( self ):
        """
        For testing purposes, update GUI
        """
        self.rootApp.update()
        self.loop.call_later( .03, self._onGuiUpdateTimeout )

    def _onDeleteWindow( self ):
        """
        Disconnect, stop / close loop
        """
        if self.Ib is not None:
            self.Ib.disconnect()

        self.loop.stop()

    def run_forever( self ):
        self._onGuiUpdateTimeout()
        self.loop.run_forever()



if __name__ == "__main__":

    """
    Some Unit Testing
    """

    logging.basicConfig(level=logging.INFO)

    util.patchAsyncio()

    #Build test application window
    root = tk.Tk()
    root.geometry( "300x200" )

    utils = Utils( rootApp=root, client = 5, asyncioloop = asyncio.get_event_loop() )


    label = ttk.Label( root, text="TWS Connection test", font = ( "Helvetica", 15, "bold" ) )
    button = ttk.Button( root, text = 'Connecto to IB', command = utils.TwsConnect )

    label.pack()
    button.pack()

    #loop = asyncio.get_event_loop()

    utils.run_forever()
