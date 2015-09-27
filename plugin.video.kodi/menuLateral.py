import re
from utils import openfile
from gravador import iniciagravador
from servidores import request_servidores

class menulateral(xbmcgui.WindowXMLDialog):

    def __init__( self, *args, **kwargs ):
            xbmcgui.WindowXML.__init__(self)
            self.finalurl = kwargs[ "finalurl" ]
            self.siglacanal = kwargs[ "siglacanal" ]
            self.name = kwargs[ "name" ]
            self.directo = kwargs[ "directo" ]

    def onInit(self):
        self.updateChannelList()

    def onAction(self, action):
        if action.getId() in [9, 10, 92, 117]:
            self.close()
            return

    def onClick(self, controlId):
        if controlId == 4001:
            self.close()
            request_servidores('','[B]%s[/B]' %(self.name))

        elif controlId == 40010:
            self.close()
            iniciagravador(self.finalurl,self.siglacanal,self.name,self.directo)

        elif controlId == 203:
            #xbmc.executebuiltin("XBMC.PlayerControl(stop)")
            self.close()

        elif controlId == 6000:
            listControl = self.getControl(6000)
            item = listControl.getSelectedItem()
            nomecanal=item.getProperty('chname')
            self.close()
            request_servidores('',nomecanal)


        #else:
        #    self.buttonClicked = controlId
        #    self.close()

    def onFocus(self, controlId):
        pass

    def updateChannelList(self):
        idx=-1
        listControl = self.getControl(6000)
        listControl.reset()
        canaison=openfile('canaison')
        canaison=canaison.replace('[','')
        lista=re.compile('B](.+?)/B]').findall(canaison)
        for nomecanal in lista:
            idx=int(idx+1)
            if idx==0: idxaux=' '
            else:
                idxaux='%4s.' % (idx)
                item = xbmcgui.ListItem(idxaux + ' %s' % (nomecanal), iconImage = '')
                item.setProperty('idx', str(idx))
                item.setProperty('chname', '[B]' + nomecanal + '[/B]')
                listControl.addItem(item)

    def updateListItem(self, idx, item):
        channel = self.channelList[idx]
        item.setLabel('%3d. %s' % (idx+1, channel.title))
        item.setProperty('idx', str(idx))

    def swapChannels(self, fromIdx, toIdx):
        if self.swapInProgress: return
        self.swapInProgress = True

        c = self.channelList[fromIdx]
        self.channelList[fromIdx] = self.channelList[toIdx]
        self.channelList[toIdx] = c

        # recalculate weight
        for idx, channel in enumerate(self.channelList):
            channel.weight = idx

        listControl = self.getControl(6000)
        self.updateListItem(fromIdx, listControl.getListItem(fromIdx))
        self.updateListItem(toIdx, listControl.getListItem(toIdx))

        listControl.selectItem(toIdx)
        xbmc.sleep(50)
        self.swapInProgress = False


