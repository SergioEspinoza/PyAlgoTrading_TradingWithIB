"""
    This

"""


class MainMenu( tk.Menu ):
    def __init__( self, container, **kwargs ):
        super().__init__( container, **kwargs )


        fileMenu = tk.Menu( self, tearoff= 0 )
        fileMenu.add_command( label='Save screener...', command=self.showSaveScreenerDialog )
        fileMenu.add_command( label='Load screener..', commmad=self.showLoadScreenerDialog )

        def showSaveScreenerDialog( self ):
            tkFileDialog.asksaveasfilename( filetypes=[( "XML", "*.xml" )])


        def showLoadScreenerDialog( self ):
            tkFileDialog.askopenfilename( filetypes=[( "XML", "*.xml" )] )


        def saveScreener( self, filename ):
            """
                arguments:
                    filename: xml file output name
                Save current bull put screener settings into xml format
                file:
                <?xml version="1.0" encoding="UTF-8"?>
                    < parameter >
                        <name>"parameter1Name"</name>
                        <value>float</value>
                    < /parameter >

                    < parameter >
                        < name>
                    < /parameter >
                        ...
                </xml>
            """
            #TODO
            pass

        def loadScreener( self, filename ):
            """
            TODO:
                load screener parameters from xml file
            """
            pass
