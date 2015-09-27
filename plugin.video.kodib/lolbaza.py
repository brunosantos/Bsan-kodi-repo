
class lolbaza(xbmcgui.WindowXMLDialog):

    def __init__( self, *args, **kwargs ):
          xbmcgui.WindowXML.__init__(self)

    def onInit(self):
        pass

    def onClick(self,controlId):
        if controlId == 2001: self.close()