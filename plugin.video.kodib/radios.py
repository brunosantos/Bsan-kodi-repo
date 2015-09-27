import os
import re
from default import addDir, art, addLink, RadiosNacionaisURL, RadiosURL, mensagemprogresso, pastaperfil
from downloader import downloader
from requests import abrir_url
from resources.lib.daring import tvporpath
from utils import clean, openfile, addDir, addLink


def radios():
    addDir('[COLOR blue][B]Radios Locais[/B][/COLOR]','nada',20,tvporpath + art + 'radios-v1.png',1,'',True)
    addLink("",'','')
    link= clean(abrir_url(RadiosNacionaisURL))
    nacionais=re.compile('<div class="radiostation boxgrid">(.+?)</div>').findall(link)
    for radioindividual in nacionais:
        radiosnacionais=re.compile('<a href="http://www.radioonline.com.pt/#(.+?)".+?<img.+?src="(.+?)".+?alt="(.+?)"').findall(radioindividual)
        for idradio,imagemradio,nomeradio in radiosnacionais:
            nomeradio=nomeradio.replace('Radio ','')
            addDir(nomeradio,idradio,21,imagemradio,len(radiosnacionais),'',False)


def radioslocais():
    link= clean(abrir_url(RadiosURL))
    #addDir('Pesquisar (exclui nacionais)',RadiosURL + '?distrito=0&concelho=0&tipo=0&text=',16,'',1,'',True)
    distritos=re.compile('id="DirectorioPesquisa1_ddlDistritos">(.+?)</select>').findall(link)[0]
    distritos=distritos.replace('<option value="0"></option>','<option value="0">Todos as rádios locais</option>')
    lista=re.compile('<option value="(.+?)">(.+?)</option>').findall(distritos)
    for iddistrito,nomedistrito in lista:
        addDir(nomedistrito,RadiosURL + '?distrito=' + iddistrito + '&concelho=0&tipo=0',24,'',len(lista),'',True)
    xbmc.executebuiltin("Container.SetViewMode(501)")


def listar_radios(name,url):
    link= clean(abrir_url(url))
    radios=re.compile('<td><a href="/portalradio/conteudos/ficha/.+?radio_id=(.+?)">(.+?)</a></td><td>(.+?)</td>.+?<td align="center">').findall(link)
    for idradio,nomeradio,concelho in radios:
        addDir('[B]'+nomeradio+'[/B] ('+concelho+')',RadiosURL + 'Sintonizador/?radio_id=' + idradio + '&scope=0',21,'http://www.radio.com.pt/APR.ROLI.WEB/Images/Logos/'+ idradio +'.gif',len(radios),'',False)
    xbmc.executebuiltin("Container.SetViewMode(501)")
    paginasradios(url,link)


def paginasradios(url,link):
    try:
        pagina=re.compile('<div id="DirectorioPesquisa1_divPageSelector">.+?<b> (.+?)</b>  <a href=/portalradio/(.+?)>').findall(link)[0]
        nrpag=int(pagina[0])+1
        nrpag=str(nrpag)
        addDir('[COLOR blue]Próxima página (' + nrpag + ') >>>[/COLOR]',RadiosURL + pagina[1],24,'',1,'',True)
    except: pass


def radiosobterurlstream(name,url):
    #GA("None","Radio - " + name)
    mensagemprogresso.create('TV Portuguesa','A carregar...')
    mensagemprogresso.update(0)
    if re.search('www.radios.pt',url):
        link=abrir_url(url)
        try:
            endereco=re.compile('<param name="url" value="(.+?)"').findall(link)[0]
        except:
            xbmc.executebuiltin("XBMC.Notification(Fightnight Music,Não é possível ouvir esta rádio.,'500000',)")
            return
        idradio=url.replace('http://www.radios.pt/portalradio/Sintonizador/?radio_id=','').replace('&scope=0','')
        thumbnail='http://www.radio.com.pt/APR.ROLI.WEB/Images/Logos/'+ idradio +'.gif'
    else:
        urlfinal='http://www.radioonline.com.pt/ajax/player.php?clear_s_name=' + url
        link= clean(abrir_url(urlfinal))
        try: player=re.compile('soundManager.createSound\({(.+?)autoLoad').findall(link)[0]
        except: player=False
        try:
            endereco=re.compile('url: "(.+?)"').findall(player)[0].replace(';','')
            if re.search('serverURL',player):
                rtmp=re.compile('serverURL: "(.+?)"').findall(player)[0]
                #rtmp=rtmp.replace('rtmp://195.23.102.206','rtmp://195.23.102.209') #tempfix
                rtmp=rtmp.replace(':1936','') #tempfix
                endereco=rtmp + ' playPath=' + endereco

        except:endereco=False
        if not endereco:
            try:endereco=re.compile('<param name="URL" value="(.+?)"').findall(link)[0]
            except:
                try: endereco=re.compile('<object data="(.+?)"').findall(link)[0]
                except: endereco=False

        if not endereco:
            xbmc.executebuiltin("XBMC.Notification(TV Portuguesa,Não é possível ouvir esta rádio.,'500000',)")
            mensagemprogresso.close()
            return

        try:thumbnail=re.compile('<img id="station-logo-player" src="(.+?)"').findall(link)[0]
        except: thumbnail=''
        if re.search('.asx',endereco):
            nomeasx='stream.asx'
            path = xbmc.translatePath(os.path.join(pastaperfil))
            lib=os.path.join(path, nomeasx)
            downloader(endereco,lib)
            texto= openfile(nomeasx)
            endereco = xbmc.PlayList(1)
            endereco.clear()
            streams=re.compile('<ref.+?"(.+?)"/>').findall(texto)
            for musica in streams:
                listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
                listitem.setInfo("music", {"Title":name})
                endereco.add(musica,listitem)
        else: pass
    mensagemprogresso.close()
    listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
    listitem.setInfo("music", {"Title":name})
    xbmc.Player().play(endereco,listitem)