# -*- coding: utf-8 -*-

""" TV Tuga
    2015 bsan"""
    
    #have a look at http://www.tvgente.me/front.php
    #ligacao.append('http://antena24.com/sic.php')   
    #http://ptcanal.com/sic-online/   
    #http://pastebin.com/raw.php?i=jY7R3fBN

import os

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
from canais import canais
from descobrirResolver import descobrirresolver, _descobrirresolver
from gravador import menugravador
from listas import listascanais, obter_lista
from mensagens import mensagemaviso, testejanela
from menuPrincipal import menu_principal
from praias import praias
from programacao import programacao_canal
from radios import radios, radioslocais, listar_radios, radiosobterurlstream
from remoteDebugger import appendPydevRemoteDebugger
from resources.lib.daring import *
from resources.lib.net import Net
from servidores import request_servidores
from utils import checker
from videoPlayer import comecarvideo

appendPydevRemoteDebugger()

net = Net()

versao = '0.1.02'
#This list should be a dictionary...
RadiosNacionaisURL = 'http://www.radioonline.com.pt'
BeachcamURL = 'http://beachcam.sapo.pt/'
CanalHDURL = 'http://canalhd.tv/tv/'
SurflineURL= 'http://www.surfline.com'
SurftotalURL='http://www.surftotal.com'
RadiosURL = 'http://www.radios.pt/portalradio/'
MEOURL = 'http://www.meocanaltv.com'
RedwebURL = 'http://www.redweb.tv'
SptveuURL = 'http://www.gosporttv.com/'
TVGOURL = 'http://www.tvgo.be/'
TVDezURL = 'http://www.estadiofutebol.com'
TVGenteURL = 'http://www.tvgente.me'
TVTugaURL = 'http://www.tvtuga.com'
TugastreamURL = 'http://www.tugastream.com/'
TVPTHDURL = 'http://www.tvportugalhd.eu'
TVPTHDZuukURL = 'http://www.zuuk.pw'
TVCoresURL = 'http://mytvfree.me'
LSHDURL= 'http://livesoccerhq.com'
TVZuneURL = 'http://www.tvzune.tv/'
TVZune2URL = 'http://soft.tvzune.co/'
RTPURL='http://www.rtp.pt'
VBURL= 'http://www.videosbacanas.com/'
ResharetvURL = 'http://resharetv.com/'
AltasEmocoesURL='http://sportslive.me/'
DesgrURL = 'http://www.desportogratis.com/'
PATH = "XBMC_TVPOR"
UATRACK="UA-39199007-1"
activado=False
user_agent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
addon_id = 'plugin.video.tvtuga'
art = '/resources/art/'
selfAddon = xbmcaddon.Addon(id=addon_id)
tvporpath = selfAddon.getAddonInfo('path')
mensagemok = xbmcgui.Dialog().ok
menuescolha = xbmcgui.Dialog().select
mensagemprogresso = xbmcgui.DialogProgress()
pastaperfil = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
cachepath = os.path.join(tvporpath,'resources','cache')
downloadPath = selfAddon.getSetting('pastagravador')
gravadorpath = os.path.join(selfAddon.getAddonInfo('path'),'resources','gravador')
activadoextra=[]
debug=[]

if not os.path.exists(tvporpath):
    tvporpath = tvporpath.decode('utf-8')
    cachepath = cachepath.decode('utf-8')
    pastaperfil = pastaperfil.decode('utf-8')
    downloadPath = downloadPath.decode('utf-8')
    gravadorpath = gravadorpath.decode('utf-8')


### LISTA CANAIS ###############


### PRAIAS ####
### PROGRAMACAO ####
### RADIOS ####
### MENSAGENS ###
### LISTAS ###
### PLAYER ####
### GRAVADOR ###
### TESTES ###

def libalternativo(finalurl):
    if xbmc.getCondVisibility('system.platform.windows'):
        import newrtmp
        finalurl,spsc=newrtmp.start_stream(rtmp=finalurl)
    else: spsc=''
    return finalurl,spsc

### REQUESTS ###
### OTHERS ###
### DOWNLOADER ###
### GA ###
### PASTAS E AFINS ###

def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'): params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2: param[splitparams[0]]=splitparams[1]
    return param

params=get_params()
url=None
thumb=None
name=None
mode=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: thumb=urllib.unquote_plus(params["thumb"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass

checker()

if mode==None or url==None or len(url)<1:
    print "Versao Instalada: v" + versao
    if selfAddon.getSetting('termos') == 'true':
        mensagemaviso()
        selfAddon.setSetting('termos',value='false')
    canais()
if mode==1: menu_principal()
elif mode==2: replaytv()
elif mode==3: replaytv_lista(name,url)
elif mode==4: replaytv_progs(name,url)
elif mode==5: obter_lista(name,url)
elif mode==6: listascanais()
elif mode==7: descobrirresolver(url,nomecanal,linkrecebido,zapping)
elif mode==8: replaytv_play(name,url)
elif mode==9: xbmc.executebuiltin("Container.NextViewMode")
elif mode==10: replaytv_pesquisa()
elif mode==11: obter_lista(name,url)
elif mode==12: menugravador()
elif mode==13: abrir_lista_canais()
elif mode==14: ok = mensagemok('TV Portuguesa','[B][COLOR white]Queres adicionar a tua lista (XML)?[/COLOR][/B]','Visita [B]http://bit.ly/fightnightaddons[/B]','ou contacta "fightnight.addons@gmail.com')
elif mode==15: ok = mensagemok('TV Portuguesa','A actualizacao é automática. Caso nao actualize va ao','repositorio fightnight e prima c ou durante 2seg','e force a actualizacao. De seguida, reinicie o XBMC.')
elif mode==16: request_servidores(url,name)
elif mode==17: comecarvideo(url,name,'listas',False,thumb=thumb)
elif mode==18: entraraddon()
elif mode==19: radios()
elif mode==20: radioslocais()
elif mode==21: radiosobterurlstream(name,url)
elif mode==22: selfAddon.openSettings()
elif mode==23: mensagemaviso()
elif mode==24: listar_radios(name,url)
elif mode==25: sportsdevil()
elif mode==26: praias()
elif mode==27: _descobrirresolver(url,name,False,False,'Praias')
elif mode==28: eventosdesportivos()
elif mode==29: firstrow()
elif mode==30: request_servidores(url,name,gravador=True)
elif mode==31: programacao_canal()
elif mode==2013: testejanela()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
