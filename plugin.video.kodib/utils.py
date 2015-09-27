import datetime
import os
import re
import sys
import urllib
import urllib2
from default import mensagemok, pastaperfil
from requests import abrir_url
from resources.lib.daring import selfAddon, user_agent


def versao_disponivel():
    try:
        link=abrir_url('http://fightnight-xbmc.googlecode.com/svn/addons/fightnight/plugin.video.tvpor/addon.xml')
        match=re.compile('name="TV Portuguesa"\r\n       version="(.+?)"\r\n       provider-name="fightnight">').findall(link)[0]
    except:
        ok = mensagemok('TV Portuguesa','Addon não conseguiu conectar ao servidor','de actualização. Verifique a situação.','')
        match='Erro. Verificar origem do erro.'
    return match


def checker():
    if selfAddon.getSetting('ga_visitor')=='':
        from random import randint
        selfAddon.setSetting('ga_visitor',str(randint(0, 0x7fffffff)))
    #checkGA()


def limparcomentarioshtml(link,url_frame):
    print "A limpar: " + url_frame
    if re.search('Sporttv1-veetle-iframe',url_frame) or re.search('Sporttv2-veetle-iframe',url_frame):
        return link
    else:
        link=clean(link)
        htmlcomments=re.compile('<!--(?!<!)[^\[>].*?-->').findall(link)
        for comentario in htmlcomments:
            if comentario[-5:]=='//-->': pass
            else:link=link.replace(comentario,'oioioioi')
        return link


def clean(text):
    command={'\r':'','\n':'','\t':'','&nbsp;':'','&#231;':'ç','&#201;':'É','&#233;':'é','&#250;':'ú','&#227;':'ã','&#237;':'í','&#243;':'ó','&#193;':'Á','&#205;':'Í','&#244;':'ô','&#224;':'à','&#225;':'á','&#234;':'ê','&#211;':'Ó','&#226;':'â'}
    regex = re.compile("|".join(map(re.escape, command.keys())))
    return regex.sub(lambda mo: command[mo.group(0)], text)


def redirect(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', user_agent)
    response = urllib2.urlopen(req)
    gurl=response.geturl()
    return gurl


def millis():
      import time as time_
      return int(round(time_.time() * 1000))


def horaportuguesa(sapo):
    if sapo==True or sapo=='diaseguinte': fmt = '%Y-%m-%d%%20%H:%M'
    else: fmt = '%Y-%m-%d %H-%M-%S'

    if selfAddon.getSetting('horaportuguesa') == 'true':
        dt  = datetime.datetime.now()
        if sapo=='diaseguinte':
            dts = dt.strftime('%Y-%m-') + str(int(dt.strftime('%d')) + 1) +dt.strftime('%%20%H:%M')
            #special dia seguinte case
        else: dts = dt.strftime(fmt)
        return dts
    else:
        from resources.lib import pytzimp
        dt  = datetime.datetime.now()
        timezona= selfAddon.getSetting('timezone2')
        terradamaquina=str(pytzimp.timezone(pytzimp.all_timezones[int(timezona)]))
        if sapo=='diaseguinte': dia=int(dt.strftime('%d')) + 1
        else: dia=int(dt.strftime('%d'))
        d = pytzimp.timezone(terradamaquina).localize(datetime.datetime(int(dt.strftime('%Y')), int(dt.strftime('%m')), dia, hour=int(dt.strftime('%H')), minute=int(dt.strftime('%M'))))
        lisboa=pytzimp.timezone('Europe/Lisbon')
        convertido=d.astimezone(lisboa)

        dts=convertido.strftime(fmt)
        return dts


def extract(_in,_out,dp=None,type='all'):
    import zipfile
    if type=='all':
        if dp:
            return allWithProgress(_in, _out, dp)

        return allNoProgress(_in, _out)

    elif type=='allNoProgress':
        try:
            zin = zipfile.ZipFile(_in, 'r')
            zin.extractall(_out)
        except Exception, e:
            print str(e)
            return False
        return True

    elif type=='allWithProgress':
        zin = zipfile.ZipFile(_in,  'r')
        nFiles = float(len(zin.infolist()))
        count  = 0
        try:
            for item in zin.infolist():
                count += 1
                update = count / nFiles * 100
                dp.update(int(update))
                zin.extract(item, _out)
        except Exception, e:
            print str(e)
            return False
        return True


def normalize(text):
    if isinstance(text, str):
        try:
            text = text.decode('utf8')
        except:
            try:
                text = text.decode('latin1')
            except:
                text = text.decode('utf8', 'ignore')
    import unicodedata
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore')


def limpar(text):
    command={'(':'- ',')':''}
    regex = re.compile("|".join(map(re.escape, command.keys())))
    return regex.sub(lambda mo: command[mo.group(0)], text)


def savefile(filename, contents,pastafinal=pastaperfil):
    try:
        destination = os.path.join(pastafinal,filename)
        fh = open(destination, 'wb')
        fh.write(contents)
        fh.close()
    except: print "Nao gravou os temporarios de: %s" % filename


def openfile(filename,pastafinal=pastaperfil):
    try:
        destination = os.path.join(pastafinal, filename)
        fh = open(destination, 'rb')
        contents=fh.read()
        fh.close()
        return contents
    except:
        print "Nao abriu os temporarios de: %s" % filename
        return None


def addDir(name,url,mode,iconimage,total,descricao,pasta):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name, "overlay":6 ,"plot":descricao} )
    liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)


def addLink(name,url,iconimage):
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
    try:
        if re.search('HD',name) or re.search('1080P',name) or re.search('720P',name):liz.addStreamInfo( 'video', { 'Codec': 'h264', 'width': 1280, 'height': 720 } )
        else: liz.addStreamInfo( 'video', { 'Codec': 'h264', 'width': 600, 'height': 300 } )
    except: pass
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)


def addCanal(name,url,mode,iconimage,total,descricao):
    cm=[]
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)#+"&thumb="+urllib.quote_plus(iconimage)
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name, "overlay":6 ,"plot":descricao} )
    liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
    try:
        if re.search('HD',name) or re.search('1080P',name) or re.search('720P',name):liz.addStreamInfo( 'video', { 'Codec': 'h264', 'width': 1280, 'height': 720 } )
        else: liz.addStreamInfo( 'video', { 'Codec': 'h264', 'width': 600, 'height': 300 } )
    except: pass
    cm.append(('Gravar canal', "XBMC.RunPlugin(%s?mode=%s&name=%s&url=%s)"%(sys.argv[0],30,name,url)))
    cm.append(('Ver programação', "XBMC.RunPlugin(%s?mode=%s&name=%s&url=%s)"%(sys.argv[0],31,name,url)))
    liz.addContextMenuItems(cm, replaceItems=False)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=total)