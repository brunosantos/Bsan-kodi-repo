import re
import sys
from default import activado, activadoextra, art, mensagemprogresso
from gravador import iniciagravador
from menuLateral import menulateral
from resources.lib.daring import tvporpath, selfAddon




def comecarvideo(finalurl,name,directo,zapping,thumb=''):
    if activado==True: activadoextra.append(finalurl)
    else: comecarvideo2(finalurl,name,directo,zapping,thumb='')


def comecarvideo2(finalurl,name,directo,zapping,thumb=''):
    if thumb=='':thumb=tvporpath + art + 'vercanais-ver2.png'
    listacanaison=selfAddon.getSetting("listacanais2")
    siglacanal=''
    namega=name.replace('-','')
    #GA("player",namega)
    if directo==True:
        thumb=name.replace('Mais TVI-','maistvi-ver2.png').replace('AXN-','axn-ver2.png').replace('FOX-','fox-ver2.png').replace('RTP 1-','rtp1-ver2.png').replace('RTP 2-','rtp2-ver2.png').replace('SIC-','sic-ver3.png').replace('SPORTTV 1-','sptv1-ver2.png').replace('SPORTTV 1 HD-','sptvhd-ver2.png').replace('SPORTTV 2-','sptv2-ver2.png').replace('SPORTTV 3-','sptv3-ver2.png').replace('SPORTTV 4-','sptv4-ver2.png').replace('SPORTTV 5-','sptv5-ver2.png').replace('SPORTTV LIVE-','sptvlive-ver1.png').replace('TVI-','tvi-ver2.png').replace('Discovery Channel-','disc-ver2.png').replace('AXN Black-','axnb-ver2.png').replace('AXN White-','axnw-ver2.png').replace('FOX Crime-','foxc-ver2.png').replace('FOX Life-','foxl-ver3.png').replace('FOX Movies-','foxm-ver2.png').replace('Eurosport-','eusp-ver2.png').replace('Hollywood-','hwd-ver2.png').replace('MOV-','mov-ver2.png').replace('Canal Panda-','panda-ver2.png').replace('VH1-','vh1-ver2.png').replace('Benfica TV 1-','btv1-ver1.png').replace('Benfica TV 2-','btv2-ver1.png').replace('Porto Canal-','pcanal-ver2.png').replace('Big Brother VIP-','bbvip-ver2.png').replace('SIC K-','sick-ver2.png').replace('SIC Mulher-','sicm-ver3.png').replace('SIC Noticias-','sicn-ver2.png').replace('SIC Radical-','sicrad-ver2.png').replace('TVI24-','tvi24-ver2.png').replace('TVI Ficção-','tvif-ver2.png').replace('Syfy-','syfy-ver1.png').replace('Odisseia-','odisseia-ver1.png').replace('História-','historia-ver1.png').replace('National Geographic Channel-','natgeo-ver1.png').replace('MTV-','mtv-ver1.png').replace('CM TV-','cmtv-ver1.png').replace('RTP Informação-','rtpi-ver1.png').replace('Disney Channel-','disney-ver1.png').replace('Motors TV-','motors-ver1.png').replace('ESPN-','espn-ver1.png').replace('Fashion TV-','fash-ver1.png').replace('A Bola TV-','abola-ver1.png').replace('Casa dos Segredos 5-','casadseg-ver1.png').replace('RTP Açores-','rtpac-ver1.png').replace('RTP Internacional-','rtpint-ver1.png').replace('RTP Madeira-','rtpmad-ver1.png').replace('RTP Memória-','rtpmem-ver1.png').replace('RTP Africa-','rtpaf-ver1.png').replace('Panda Biggs-','pbiggs-ver1.png').replace('TV Record-','record-v1.png').replace('TV Globo-','globo-v1.png').replace('Eurosport 2-','eusp2-ver1.png').replace('Discovery Turbo-','discturbo-v1.png').replace('Toros TV-','toros-v1.png').replace('Chelsea TV-','chel-v1.png').replace('Disney Junior-','djun-ver1.png').replace('Económico TV-','econ-v1.png').replace('Caça e Pesca-','cacapesca-v1.png').replace('Sporting TV-','scptv-ver1.png').replace('Euronews-','euronews-ver1.png').replace('TPA Internacional-','tpa-ver1.png').replace('ARTV-','artv-ver1.png').replace('TRACE Urban-','traceu.png').replace('Virgin Radio TV-','virginr.png').replace('DJing TV-','djingtv.png')
        name=name.replace('-','')
        progname=name

        siglacanal=name.replace('SPORTTV 1','SPTV1').replace('SPORTTV 2','SPTV2').replace('SPORTTV 3','SPTV3').replace('SPORTTV 4','SPTV4').replace('SPORTTV 5','SPTV5').replace('SPORTTV LIVE','SPTVL').replace('Discovery Channel','DISCV').replace('AXN Black','AXNBL').replace('AXN White','AXNWH').replace('FOX Crime','FOXCR').replace('FOX Life','FLIFE').replace('FOX Movies','FOXM').replace('Eurosport','EURSP').replace('Hollywood','HOLLW').replace('Canal Panda','PANDA').replace('Benfica TV 1','SLB').replace('Benfica TV 2','SLB2').replace('Porto Canal','PORTO').replace('SIC K','SICK').replace('SIC Mulher','SICM').replace('SIC Noticias','SICN').replace('SIC Radical','SICR').replace('TVI24','TVI24').replace('TVI Ficção','TVIFIC').replace('Mais TVI','SEM').replace('Syfy','SYFY').replace('Odisseia','ODISS').replace('História','HIST').replace('National Geographic Channel','NGC').replace('MTV','MTV').replace('CM TV','CMTV').replace('RTP Informação','RTPIN').replace('Disney Channel','DISNY').replace('Motors TV','MOTOR').replace('ESPN America','SEM').replace('Fashion TV','FASH').replace('MOV','SEM').replace('A Bola TV','ABOLA').replace('Panda Biggs','BIGGS').replace('RTP 1','RTP1').replace('RTP 2','RTP2').replace('RTP Açores','RTPAC').replace('RTP Madeira','RTPMD').replace('RTP Memória','RTPM').replace('Disney Junior','DISNYJ').replace('RTP Africa','RTPA').replace('Económico TV','ETVHD').replace('Chelsea TV','CHELS').replace('TV Globo','GLOBO').replace('TV Record','TVREC').replace('Eurosport 2','EURS2').replace('Discovery Turbo','DISCT').replace('Toros TV','TOROTV').replace('Caça e Pesca','CAÇAP').replace('Sporting TV','SCP').replace('TPA Internacional','TPA')
        listitem = xbmcgui.ListItem(progname, iconImage="DefaultVideo.png", thumbnailImage=tvporpath + art + thumb)
    else: listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumb)
    if zapping==True and not re.search('.f4m',finalurl):
        #conteudoficheiro=openfile(('zapping'))
        #savefile(('zapping', conteudoficheiro + '_comeca_' + name + '_nomecanal_' + finalurl + '_thumb_' + thumb + '_acaba_'))
        iniciagravador(finalurl,siglacanal,name,directo)
    else:

        if re.search('.f4m',finalurl):
            from resources.lib.proxyf4m import f4mProxyHelper
            helper=f4mProxyHelper()
            finalurl,spscpid = helper.start_proxy(finalurl, name)
        else:
            #finalurl,spscpid=libalternativo(finalurl)
            spscpid='nada'

        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem.setInfo("Video", {"Title":name})
        listitem.setProperty('IsPlayable', 'true')
        if finalurl=='http://live.2caster.com:1935/live/sica/playplist.m3u8':finalurl=''
        playlist.add(finalurl, listitem)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]),True,listitem)
        mensagemprogresso.close()
        dialogWait = xbmcgui.DialogProgress()
        dialogWait.create('TV Portuguesa', 'A carregar...')
        dialogWait.close()
        del dialogWait

        player = Player(finalurl=finalurl,name=name,siglacanal=siglacanal,directo=directo,spscpid=spscpid)
        if "RunPlugin" in finalurl:
            xbmc.executebuiltin(finalurl)
        else:

            player.play(playlist)
            lat123 = menulateral("menulateral.xml" , tvporpath, "Default",finalurl=finalurl,name=name,siglacanal=siglacanal,directo=directo)

            while player.is_active:
                if listacanaison == "true":
                    if xbmc.getCondVisibility('Window.IsActive(videoosd)') and directo==True:
                        xbmc.executebuiltin('XBMC.Control.Move(videoosd,9999)')
                        lat123.doModal()
                        while xbmc.getCondVisibility('Window.IsActive(videoosd)'): pass
                player.sleep(1000)

            #if not player.is_active:
            #    print "Parou. Saiu do ciclo."
            #    sys.exit(0)

                #player.sleep(10000)
            #print "ERRO"


class Player(xbmc.Player):
      def __init__(self,finalurl,name,siglacanal,directo,spscpid):
            if selfAddon.getSetting("playertype") == "0": player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
            elif selfAddon.getSetting("playertype") == "1": player = xbmc.Player(xbmc.PLAYER_CORE_MPLAYER)
            elif selfAddon.getSetting("playertype") == "2": player = xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER)
            elif selfAddon.getSetting("playertype") == "3": player = xbmc.Player(xbmc.PLAYER_CORE_PAPLAYER)
            else: player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
            self.is_active = True
            self._refInfo = True
            self._totalTime = 999999
            self._finalurl=finalurl
            self._name=name
            self._siglacanal=siglacanal
            self._directo=directo
            self._spscpid=spscpid
            print "Criou o player"
            #player.stop()

      def onPlayBackStarted(self):
            print "Comecou o player"

      def onPlayBackStopped(self):
            print "Parou o player"
            self.is_active = False
            if re.search('.f4m',self._finalurl): self._spscpid.set()
            #import newrtmp
            #newrtmp.stop_stream(self._spscpid)
            #opcao= xbmcgui.Dialog().yesno("TV Portuguesa", "Este stream funciona? ", "(exemplificação / ainda não funciona)", "",'Sim', 'Não')
            ###### PERGUNTAR SE O STREAM E BOM #####

      def onPlayBackEnded(self):
            self.onPlayBackStopped()
            print 'Chegou ao fim. Playback terminou.'


      def sleep(self, s): xbmc.sleep(s)


