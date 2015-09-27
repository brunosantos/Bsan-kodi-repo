from lolbaza import lolbaza
from menuLateral import menulateral
from resources.lib.daring import selfAddon, tvporpath


def mensagemaviso():
    try:
        xbmc.executebuiltin("ActivateWindow(10147)")
        window = xbmcgui.Window(10147)
        xbmc.sleep(100)
        window.getControl(1).setLabel( "%s - %s" % ('AVISO','TV Portuguesa',))
        window.getControl(5).setText("buuuu")
    except: pass


def sintomecomsorte():
    if selfAddon.getSetting("mensagemgratis3") == "true":
        d = lolbaza("lolbaza.xml" , tvporpath, "Default")
        d.doModal()
        del d
        selfAddon.setSetting('mensagemgratis3',value='false')


def librtmpwindow():
    if selfAddon.getSetting("rtmp-lib0001") == "false":
        d = lolbaza("librtmp.xml" , tvporpath, "Default")
        d.doModal()
        del d


def testejanela():
    d = menulateral("menulateral.xml" , tvporpath, "Default")
    d.doModal()
    del d