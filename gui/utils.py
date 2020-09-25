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

@dataclass
class Utils( ):

    #timeout (seconds)
    timeout = 5
    host = "127.0.0.1"
    port = 7497


    def __init__( self, asyncioloop = None,  client: int = 1, msgBoxParent = None,   ):

        self.Ib = None
        self.clientId = client
        self.connected = False
        self.msgBoxParent = msgBoxParent
        self.loop = asyncioloop


    def onDisconnected( self ):
        self.connected = False

        if self.msgBoxParent != None:
            messagebox.showinfo( title = "Connection Timeout",
                                 message = "Client Disconnected!",
                                 parent = self.msgBoxParent )

    def onConnected( self ):
        self.connected = True
        self.progressDialog.destroy()

        if self.msgBoxParent != None:
            messagebox.showinfo( title = "Connected!!",
                                 message = f"Connected w/ client ID !!",
                                 parent=self.msgBoxParent )

    def TwsConnect( self, readOnly: bool = False ) -> bool:
        """
            Connect to IB TWS of IB gateway.
            Spawn progress dialog and notify in case of connection success

            Args:

            readOnly: Accces read only mode
            msgBoxParent: Root frame for dialog box notification

            Return:
                True if connection success
        """

        if  self.Ib == None:
            self.Ib = IB()
            self.Ib.disconnectedEvent += self.onDisconnected
            self.Ib.connectedEvent += self.onConnected


        if self.Ib.isConnected() == False:

            self.progressDialog = tk.Toplevel( self.msgBoxParent )
            progress = ttk.Progressbar( self.progressDialog, mode='indeterminate' )
            progress.place( x=30, y=60, width=200 )
            progress.start()

            self.Ib.connect( self.host,
                             self.port,
                             self.clientId,
                             timeout = self.timeout,
                             readonly = readOnly )

        elif msgBoxParent != None :
            messagebox.showinfo( "Already connected", parent=msgBoxParent )



    def _onTimeout( self ):
        """
        For testing purposes, update GUI
        """
        self.root.update()
        self.loop.call_later( .03, _onTimeout, *[root, loop] )

    def _onDeleteWindow( self ):
        """
        Disconnect, stop / close loop
        """
        self.Ib.disconnnect()
        self.loop.stop()

if __name__ == "__main__":

    """
    Some Unit Testing
    """
    def main():
        root = tk.Tk()

        root.geometry( "300x200" )

        loop = asyncio.get_event_loop()

        if loop.is_running():
             print('loop already running')

        root.protocol('WM_DELETE_WINDOW', _onDeleteWindow )

        args = [root, loop]
        loop.call_later( 0.03, _onTimeout, *[root, loop] )

        utils = Utils( msgBoxParent=root, client = 5, asyncioloop = loop )

        try:
            utils.TwsConnect( )
        except:
            print( 'Exception catched' )

        loop.run_forever()

    util.patchAsyncio()

    main()
