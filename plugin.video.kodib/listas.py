import re
import sys
from default import addDir, art, addCanal, mensagemok
from requests import abrir_url
from videoPlayer import comecarvideo
from resources.lib.daring import tvporpath, selfAddon
from utils import clean, addDir, addCanal


def listascanais():
    addDir("[B]Desporto[/B] (cesarix)",'http://dl.dropboxusercontent.com/u/266138381/Desporto.xml',5,tvporpath + art + 'ces-desp-ver1.png',1,'',True)
    addDir("[B]Desporto/Global[/B] (vdubt25)",'http://bit.ly/vdubt25',5,tvporpath + art + 'listas-ver2.png',1,'',True)
    addDir("[B]Global[/B] (magellan)",'http://goo.gl/aOLLyX',5,tvporpath + art + 'listas-ver2.png',1,'',True)
    addDir("[B]Global[/B] (fightnight)",'http://pastebin.com/raw.php?i=HUuni0c8',5,tvporpath + art + 'listas-ver2.png',1,'',True)
    addDir("[B]Música[/B] (cesarix)",'http://dl.dropboxusercontent.com/u/266138381/Musica.xml',5,tvporpath + art + 'ces-mus-ver1.png',1,'',True)
    addDir("[B]Ciências[/B] (cesarix)",'http://dl.dropboxusercontent.com/u/266138381/Tv%20Ciencia.xml',5,tvporpath + art + 'ces-ciencia-ver1.png',1,'',True)
    addDir("[B]Alemanha[/B] (cesarix)",'http://dl.dropboxusercontent.com/u/266138381/Tv%20Alema.xml',5,tvporpath + art + 'ces-alem-ver1.png',1,'',True)
    addDir("[B]Espanha[/B]",'http://dl.dropboxusercontent.com/u/266138381/Tv%20Espanhola.xml',5,tvporpath + art + 'ces-espa-ver1.png',1,'',True)
    addDir("[B]UK[/B] (cesarix)",'http://dl.dropboxusercontent.com/u/266138381/Tv%20UK.xml',5,tvporpath + art + 'ces-uk-ver1.png',1,'',True)
    addDir("[B]USA[/B] (cesarix)",'http://dl.dropboxusercontent.com/u/266138381/Tv%20USA.xml',5,tvporpath + art + 'ces-usa-ver1.png',1,'',True)
    addDir("[B]Global[/B] (mafarricos)",'http://dl.dropbox.com/u/88295111/pissos13.xml',5,tvporpath + art + 'pissos-ver1.png',1,'',True)
    addDir("[B]Portugal[/B]",'http://dl.dropboxusercontent.com/s/h9s0oiop70tjwe8/TV%20PORTUGUESA.txt',5,tvporpath + art + 'vercanais-ver2.png',1,'',True)
    addDir("[B]Filmes[/B]",'http://dl.dropboxusercontent.com/s/kk79s083x208zug/xml%20pt%20tv%20-%20nova.txt',5,tvporpath + art + 'vercanais-ver2.png',1,'',True)
    addDir("[B]Infantil[/B]",'http://dl.dropboxusercontent.com/s/kbly079op7kwaz2/INFANTIL%20TV%20POR.txt',5,tvporpath + art + 'vercanais-ver2.png',1,'',True)
    addDir("[B]Brasil[/B]",'http://dl.dropboxusercontent.com/s/9ilbiv4d83dlcrr/TV%20BRASILEIRA%20POR.txt',5,tvporpath + art + 'vercanais-ver2.png',1,'',True)
    #addLink("",'',tvporpath + art + 'listas-ver2.png')
    if selfAddon.getSetting("listasextra") == "true":
        try:listasextras()
        except:pass

    addDir("[B][COLOR white]A tua lista aqui?[/COLOR][/B]",'nada',14,tvporpath + art + 'versao-ver2.png',1,'',False)
    #xbmc.executebuiltin("Container.SetViewMode(500)")


def listasextras():
    iptvurl='http://01.gen.tr/HasBahCa_IPTV/'
    link= clean(abrir_url(iptvurl))
    streams=re.compile('<a class="autoindex_a" href="./(.+?)">.+?<td class="autoindex_td_right">.+?</td.+?td class="autoindex_td_right">(.+?)</td>').findall(link)
    for nomepasta,act in streams:
        if re.search('.m3u',nomepasta):
            titulo=nomepasta.replace('.m3u','').replace('_',' ').title()
            addDir("[B]%s[/B] (act.%s)" % (titulo,act[2:-2]),iptvurl + nomepasta,5,tvporpath + art + 'listas-ver2.png',1,'',True)


def parseM3U(infile,link=False):
    if link==False: inf=abrir_url(infile).splitlines( )
    else: inf=link.splitlines( )

    playlist=[]
    musica=[]
    titulo=''
    urlstream=''
    for line in inf:
        line=line.strip()
        if line.startswith('#EXTINF:'):
            #stupid guys with spaces and common errors
            try:titulo=line.split('#EXTINF:')[1].split(',  ',1)[1]
            except:
                try:titulo=line.split('#EXTINF:')[1].split(', ',1)[1]
                except:
                    try:titulo=line.split('#EXTINF:')[1].split(',',1)[1]
                    except:titulo=line.split('#EXTINF:')[1].split('" ',1)[1]
        elif re.search('#EXTM3U',line):
            pass
        elif (len(line) != 0):
            line=line.replace('rtmp://$OPT:rtmp-raw=','')
            urlstream=line
            musica.append(titulo)
            musica.append(urlstream)
            musica.append(tvporpath + art + 'vercanais-ver2.png')#fakethumb
            playlist.append(musica)
            musica=[]
            titulo=''
            urlstream=''


    return playlist


def obter_lista(name,url):
    #GA("None",name)
    titles = []; ligacao = []; thumb=[]
    link=abrir_url(url)
    if re.search('.m3u',url) or re.search('#EXTM3U',link):
        listas= parseM3U(url,link)
    else:
        link2= clean(link)
        listas=re.compile('<title>(.+?)</title>(.+?)<thumbnail>(.+?)</thumbnail>').findall(link2)

    for nomecanal,streams,thumbcanal in listas:
        if re.search('<link>',streams):
            streams2=re.compile('<link>(.+?)</link>').findall(streams)
        else:
            streams2=[]
            streams2.append(streams)#ugly

        for rtmp in streams2:
#            if re.search('$doregex',rtmp):
#                #parametros=re.compile('<regex></regex>').findall(rtmp)
#                doRegexs = re.compile('\$doregex\[([^\]]*)\]').findall(rtmp)
#                    for k in doRegexs:
#
#                        if k in regexs:
#                            m = regexs[k]
#                            #if m['page'] in cachedPages:
#                            #    link = cachedPages[m['page']]
#                            #else:
#                            page=re.compile('<page>(.+?)</page>').findall(streams2)[0]
#                            req = urllib2.Request(page)
#                            req.add_header('User-Agent', user_agent)
#                            if re.search('<referer>',streams2):
#                                referer=re.compile('<referer>(.+?)</referer>').findall(streams2)[0]
#                                req.add_header('Referer', referer)
#                            response = urllib2.urlopen(req)
#                            link = response.read()
#                            response.close()
#                            expres=re.compile("""<expres>'file':'([^']*)<expres>""").findall(streams2)[0]
#                            reg = re.compile(expres).search(link)
#                            rtmp = url.replace("$doregex[" + k + "]", reg.group(1).strip())


            if name=='[B][COLOR white]Eventos[/COLOR][/B] (Cesarix/Rominhos)':
                titles.append(nomecanal)
                ligacao.append(rtmp)
                thumb.append(thumbcanal)
            else:
                addCanal(nomecanal,rtmp,17,thumbcanal,len(listas),'')
                xbmcplugin.setContent(int(sys.argv[1]), 'Movies')


    if name=='[B][COLOR white]Eventos[/COLOR][/B] (Cesarix/Rominhos)':
        if len(ligacao)==0: ok=mensagemok('TV Portuguesa', 'Sem eventos disponiveis.'); return
        else:
            if len(ligacao)==1: index=0
            else:index = xbmcgui.Dialog().select('Escolha o servidor', titles)
            if index > -1:
                urlescolha=ligacao[index]
                nomecanal=titles[index]
                #thumb123=thumbcanal[index]
                #print thumb123
                comecarvideo(urlescolha,nomecanal,'listas',False,thumb=tvporpath + art + 'vercanais-ver2.png')

