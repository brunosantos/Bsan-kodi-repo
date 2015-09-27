import os
import re
import sys
import urllib
from JsUnpacker import JsUnpackerV2
from default import activado, mensagemprogresso, abrir_url_cookie, TVCoresURL, abrir_url_tommy, mensagemok, \
    RTPURL, ResharetvURL, debug
from downloader import downloader
from requests import abrir_url, abrir_url_cookie, abrir_url_tommy
from resources.lib.daring import user_agent, selfAddon
from utils import limparcomentarioshtml, clean, redirect, millis, extract
from videoPlayer import comecarvideo


def descobrirresolver(url_frame,nomecanal,linkrecebido,zapping,nomeserver):
    marcador='A iniciar Resolvers'
    if zapping==False and activado==False: mensagemprogresso.update(50)
    try:
        yoyo265='type:"flash".+?"'
        yoyo115='file:'

        if linkrecebido==False and not url_frame[0:9]=='stream://':
            marcador="Resolver: O url da frame e " + url_frame; print marcador

            url_frame=url_frame.replace(' ','%20')
            link=abrir_url_cookie(url_frame)
            try:link= limparcomentarioshtml(link,url_frame)
            except: pass
            link= clean(link)

            link=link.replace('cdn.zuuk.net\/boi.php','').replace('cdn.zuuk.net\/stats.php','').replace('cdn.zuuk.net/boi.php','').replace('cdn.zuuk.net/stats.php','').replace('<p><script language="JavaScript"> setTimeout','<p><script language="JavaScript">setTimeout').replace('micast_ads','')

        elif url_frame[0:9]=='stream://':
            marcador="Resolver: Stream Directo"; print marcador
            link=''
        else:
            marcador="Resolver: O produto final no descobrirresolver"; print marcador
            link= limparcomentarioshtml(linkrecebido,url_frame)
            link=link.replace('<title>Zuuk.net</title>','').replace('http://s.zuuk.net/300x250.html','').replace('www.zuuk.net\/test.php?ch=','').replace('cdn.zuuk.net\/boi.php','').replace('cdn.zuuk.net\/stats.php','').replace('cdn.zuuk.net/boi.php','').replace('cdn.zuuk.net/stats.php','').replace('<p><script language="JavaScript"> setTimeout','<p><script language="JavaScript">setTimeout').replace('micast_ads','').replace('ptcanal.com/ads/300x250.php','')

        link=urllib.unquote(link)
        if url_frame[0:9]=='stream://':
            marcador="Catcher: direct stream url"; print marcador
            streamurl=url_frame.replace("stream://",'')
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search("<iframe src='http://www.zuuk.pw",link):
            marcador="Catcher: zuuk.pw"; print marcador
            name=re.compile("<iframe src='http://www.zuuk.pw(.+?)'").findall(link)[0]
            descobrirresolver('http://www.zuuk.pw' + name,nomecanal,False,zapping,nomeserver)

        elif re.search("zuuk.net",link):
            marcador="Catcher: zuuk outro"; print marcador
            #stolen zuuk patch
            if re.search('tvtuga.com',url_frame):
                url_roubado=re.compile("""setTimeout\("window.open\('(.+?)'""").findall(link)[0]
                descobrirresolver(url_roubado,nomecanal,False,zapping,nomeserver)
                return
            ##
            if re.search('<script type="text/javascript">//var urls = new Array',link): url_final=re.compile('new Array.+?"(.+?)",').findall(link)[0]
            ##derbie##

            else:
                try:name=re.compile('<iframe.+?src="http://(.+?)zuuk.net/(.+?)"').findall(link)[0]
                except:name=re.compile("""setTimeout\("window.open\('http://(.+?)zuuk.net/(.+?)'""").findall(link)[0]
                url_final="http://%szuuk.net/%s" % (name[0],name[1])

            link=abrir_url_cookie(url_final)
            link= limparcomentarioshtml(link,url_frame)
            try:
                info=re.compile("<div id='mediaspace'>"+'<script language="javascript".+?' + "document.write.+?unescape.+?'(.+?)'").findall(link)[0]
                if info=="' ) );</script> <script type=": info=False
            except:info=False
            if info: infotratada=urllib.unquote(info)
            else: infotratada=link
            if re.search('<meta http-equiv="refresh" content="0; url=',link):
                marcador="Catcher: gajos a enganar.. mesmo stream"; print marcador
                redirecturl=re.compile('<meta http-equiv="refresh" content="0; url=(.+?)"').findall(link)[0]
                url_final="http://%szuuk.net/%s" % (name[0],redirecturl)
                descobrirresolver(url_final,nomecanal,False,zapping,nomeserver)
            else: descobrirresolver(url_final,nomecanal,infotratada,zapping,nomeserver)

        elif re.search('http://cdn.zuuk.org',link):
            marcador="Catcher: zuuk.org"; print marcador
            ##derbie##
            if re.search('<script type="text/javascript">//var urls = new Array',link): url_final=re.compile('new Array.+?"(.+?)",').findall(link)[0]
            else:
                redirecturl=re.compile('src="http://([^"]+?).zuuk.([^"]+?)"').findall(link)[0]
                url_final="http://%s.zuuk.%s" % (redirecturl[0],redirecturl[1])
            descobrirresolver(url_final,nomecanal,False,zapping,nomeserver)

        elif re.search('<p><script language="JavaScript">setTimeout', link):
            marcador="Catcher: tvtuga zuuk"; print marcador
            ptcanal= redirect(re.compile('setTimeout.+?"window.open.+?' + "'(.+?)',").findall(link)[0])
            if re.search('.f4m',ptcanal):
                ptcanal=ptcanal + '&'
                descobrirresolver(ptcanal,nomecanal,ptcanal,zapping,nomeserver)
            elif re.search('rtmp://live.2caster.com',ptcanal):
                descobrirresolver(ptcanal,nomecanal,ptcanal,zapping,nomeserver)
            else:
                html=urllib.unquote(abrir_url(ptcanal))
                descobrirresolver(ptcanal,nomecanal,html,zapping,nomeserver)

        elif re.search('id="innerIframe"',link):
            marcador="Catcher: id=innerIframe"; print marcador
            link= clean(link)
            #embed=re.compile('<br/><iframe.+?src="(.+?)" id="innerIframe"').findall(link)[0]
            embed=re.compile('<iframe[^<]+?src="([^"]+?)" id="innerIframe"').findall(link)[0]
            ref_data = {'Referer': url_frame,'User-Agent':user_agent}
            #urlembed = embed
            urlembed=TVCoresURL + embed
            urlembed=urlembed.replace('http://mytvfree.mehttp://antena.mytvfree.me','http://antena.mytvfree.me/')
            html = abrir_url_tommy(urlembed,ref_data)
            descobrirresolver(urlembed,nomecanal,html,zapping,nomeserver)


        #### ALIVE REMOVER DEPOIS ####

        #elif re.search('file=myStream.sdp',link) or re.search('ec21.rtp.pt',link):
        #    marcador="Catcher: RTP Proprio"; print marcador
        #    #link=abrir_url_cookie(url_frame)
            #urlalive=re.compile('<iframe src="(.+?)".+?></iframe>').findall(link)[0]
            #import cookielib
            #cookie = cookielib.CookieJar()
            #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
            #opener.addheaders = [('Host','www.rtp.pt'), ('User-Agent', user_agent), ('Referer',url_frame)]
            #linkfinal = opener.open(urlalive).read()
        #    rtmpendereco=re.compile('streamer=(.+?)&').findall(link)[0]
        #    filepath=re.compile('file=(.+?)&').findall(link)[0]
        #    filepath=filepath.replace('.flv','')
        #    swf="http://player.longtailvideo.com/player.swf"
        #    streamurl=rtmpendereco + ' playPath=' + filepath + ' swfUrl=' + swf + ' live=1 timeout=15 pageUrl=' + url_frame
        #    comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('04stream',link):
            marcador="Catcher: 04stream"; print marcador
            try:rtmp=re.compile('file=(.+?)"').findall(link)[0]
            except: rtmp=re.compile('file=(.+?)&amp;').findall(link)[0]
            try:swf=re.compile('type="application/x-shockwave-flash" class=".+?" src="(.+?)"').findall(link)[0]
            except:swf=re.compile('src="([^"]+?)" class=".+?" type="application/x-shockwave-flash"').findall(link)[0]

            streamurl=rtmp + ' swfUrl=' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=http://www.04stream.com'
            comecarvideo(streamurl,nomecanal,True,zapping)


        elif re.search('720Cast',link) or re.search('ilive',link):
            marcador="Catcher: ilive"; print marcador
            setecast=re.compile("fid='(.+?)';.+?></script>").findall(link)

            if not setecast: setecast=re.compile('file: ".+?/app/(.+?)/.+?",').findall(link)
            if not setecast: setecast=re.compile('flashvars="file=(.+?)&').findall(link)
            if not setecast: setecast=re.compile('src="/ilive.tv.php.+?id=(.+?)" id="innerIframe"').findall(link)
            if not setecast: setecast=re.compile('http://www.ilive.to/embed/(.+?)&').findall(link)
            if not setecast: setecast=re.compile('http://www.ilive.to/embedplayer.php.+?&channel=(.+?)&').findall(link)
            for chname in setecast:
                embed='http://www.ilive.to/embedplayer.php?width=640&height=400&channel=' + chname + '&autoplay=true'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                if '<script language=javascript>c="' in html:
                    from resources.lib import ioncube
                    html=ioncube.ioncube1(html)

                tempomili=str(millis())
                urltoken=re.compile(""".*getJSON\("([^'"]+)".*""").findall(html)[0] + '&_='+ tempomili
                urltoken2= abrir_url_tommy(urltoken,ref_data)
                token=re.compile('"token":"(.+?)"').findall(urltoken2)[0]
                rtmp=re.compile('streamer: "(.+?)",').findall(html)[0].replace('\\','')
                filelocation=re.compile('file: "(.+?).flv",').findall(html)[0]
                swf=re.compile("type: 'flash', src: '(.+?)'").findall(html)[0]
                app=re.compile('rtmp://[\.\w:]*/([^\s]+)').findall(rtmp)[0]
                streamurl=rtmp + ' app=' + app+' playPath=' + filelocation + ' swfUrl=' + swf + ' token='+ token +' swfVfy=1 live=1 timeout=15 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('2caster',link) or re.search('4caster',link):
            marcador="Catcher: 2caster"; print marcador
            try:
                rtmp=re.compile('streamer=(.+?)&').findall(url_frame)[0]
                filep=re.compile('file=(.+?)&').findall(url_frame)[0]
            except:
                rtmp=re.compile('streamer=(.+?)&').findall(link)[0]
                filep=re.compile('file=(.+?)&').findall(link)[0]
            streamurl=rtmp + ' playPath=' + filep + ' live=true timeout=15 swfUrl=http://player.longtailvideo.com/player.swf pageUrl=' + url_frame
                #streamurl='http://live.2caster.com:1935/live/' + filep + '/playplist.m3u8'
            #else:
            #    swf=re.compile('<param name="src" value="(.+?)\?').findall(link)[0]
            #    streamurl=filep.replace('rtmp://live.2caster.com/live/','http://live.2caster.com:1935/live/') + '/playplist.m3u8'


            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('9stream',link):
            marcador="Catcher: 9stream"; print marcador
            stream=re.compile('src="http://www.9stream.com/embed/(.+?)&').findall(link)
            for chid in stream:
                embed='http://www.9stream.com/embedplayer.php?width=650&height=400&channel=' + chid + '&autoplay=true'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                if '<script language=javascript>c="' in html:
                    from resources.lib import ioncube
                    html=ioncube.ioncube1(html)
                    #if re.search('window.open\("http://www.direct2watch.com',html):
                    #    frame=re.compile('window.open\("http://www.direct2watch.com(.+?)"\)').findall(html)[0]
                    #    ref_data = {'Referer': embed,'User-Agent':user_agent}
                    #    html= abrir_url_tommy('http://www.direct2watch.com' + frame,ref_data)
                    #    html=ioncube.ioncube1(html)
                tempomili=str(millis())
                urltoken=re.compile(""".*getJSON\("([^'"]+)".*""").findall(html)[0] + '&_='+ tempomili
                urltoken2= abrir_url_tommy(urltoken,ref_data)

                token=re.compile('"token":"(.+?)"').findall(urltoken2)[0]
                try:rtmp=re.compile("""'streamer': "(.+?)",""").findall(html)[0].replace('\\','')
                except:rtmp=re.compile('streamer: "(.+?)",').findall(html)[0].replace('\\','')
                try:filelocation=re.compile("'file': '(.+?).flv',").findall(html)[0]
                except:filelocation=chid
                try:swf=re.compile('flashplayer: "(.+?)"').findall(html)[0]
                except:swf=re.compile("type: 'flash', src: '(.+?)'").findall(html)[0]
                app=re.compile('rtmp://[\.\w:]*/([^\s]+)').findall(rtmp)[0]
                streamurl=rtmp + ' app=' + app+' playPath=' + filelocation + ' swfUrl=' + swf + ' token='+ token +' swfVfy=1 live=1 timeout=15 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('abcast', link):
            marcador="Catcher: abcast"; print marcador
            flex=re.compile("file='(.+?)';.+?></script>").findall(link)
            for chid in flex:
                embed='http://abcast.net/embed.php?file='+chid+'&width=650&height=400'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                rtmp=re.compile("&streamer=(.+?)&").findall(html)[0]#.replace('redirect','live')
                playpath=re.compile("file=(.+?)&").findall(html)[0]
                swf=re.compile('object data="(.+?)"').findall(html)[0]
                streamurl=rtmp + ' playPath=' + playpath + ' swfUrl=http://abcast.net/'+swf+' live=true timeout=15 swfVfy=1 conn=S:OK pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('aliez',link):
            marcador="Catcher: aliez"; print marcador
            aliez=re.compile('src="http://emb.aliez.tv/player/live.php.+?id=(.+?)&').findall(link)
            for chid in aliez:
                embed='http://emb.aliez.tv/player/live.php?id=' + chid + '&w=700&h=420'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                swf=re.compile('swfobject.embedSWF\("([^"]+)"').findall(html)[0]
                rtmp=urllib.unquote(re.compile('"file":\s."([^"]+)"').findall(html)[0])
                streamurl=rtmp + ' live=true swfVfy=1 swfUrl=' + swf + ' pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('castalba', link):
            marcador="Catcher: castalba"; print marcador
            castalba=re.compile('<script type="text/javascript"> id="(.+?)";.+?></script>').findall(link)
            for chname in castalba:
                embed='http://castalba.tv/embed.php?cid=' + chname + '&wh=640&ht=385&r=cdn.thesporttv.eu'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                swf=re.compile("""flashplayer': "(.+?)",""").findall(html)[0]
                filelocation=re.compile("'file': '(.+?)',").findall(html)[0]
                rtmpendereco=re.compile("'streamer': '(.+?)',").findall(html)[0]
                streamurl=rtmpendereco + ' playPath=' + filelocation + '?id=' + ' swfUrl=http://www.udemy.com/static/flash/player5.9.swf live=true timeout=15 swfVfy=true pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('cast247',link):
            marcador="Catcher: cast247"; print marcador
            castamp=re.compile('fid="(.+?)".+?</script>').findall(link)
            for chname in castamp:
                pass #site ja nao existe

        elif re.search('castamp',link):
            marcador="Catcher: castamp"; print marcador
            castamp=re.compile('channel="(.+?)".+?</script>').findall(link)
            for chname in castamp:
                embed='http://castamp.com/embed.php?c='+chname
                ref_data = {'Referer': 'http://www.zuuk.net','User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                swf=re.compile("""flashplayer': "(.+?)",""").findall(html)[0]
                filelocation=re.compile("'file': '(.+?)',").findall(html)[0]
                rtmpendereco=re.compile("'streamer': '(.+?)',").findall(html)[0]
                streamurl=rtmpendereco + ' playPath=' + filelocation + ' swfUrl=' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search("abouttext: 'CanalHD.TV'",link):
            marcador="Catcher: canalhd.tv"; print marcador
            rtmp=re.compile("file: '(.+?)'").findall(link)[0]
            if re.search('rtmp',link):
                chid=''.join((rtmp.split('/'))[-1:])
                swf='http://canalhd.tv/tv/jwplayer/jwplayer.flash.swf'
                streamurl=rtmp.replace(chid,'') + ' playPath='+chid+' swfUrl=' + swf + ' live=true swfVfy=true pageUrl=' + url_frame
            else: streamurl=rtmp + '|User-agent=Mozilla%2F5.0%20(Linux%3B%20Android%205.0.1%3B%20Nexus%20)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F38.0.1847.114%20Mobile%20Safari%2F537.36'
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('cast3d', link): ##nao esta
            marcador="Catcher: cast3d"; print marcador
            cast3d=re.compile('fid="(.+?)";.+?></script>').findall(link)
            for chname in cast3d:
                embed='http://www.cast3d.tv/embed.php?channel=' + '&vw=640&vh=385&domain=lsh.lshunter.tv'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                swf=re.compile("""flashplayer': "(.+?)",""").findall(html)
                filelocation=re.compile("'file': '(.+?)',").findall(html)
                rtmpendereco=re.compile("'streamer': '(.+?)',").findall(html)
                streamurl=rtmpendereco[0] + ' playPath=' + filelocation[0] + '?id=' + ' swfUrl=' + swf[0] + ' live=true timeout=15 swfVfy=true pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('castfree', link):
            marcador="Catcher: castfree"; print marcador
            cenas=re.compile('castfree.net/(.+?)"').findall(link)[0]
            ref_data = {'Referer': url_frame,'User-Agent':user_agent}
            framesite='http://castfree.net/' + cenas
            html= abrir_url_tommy(framesite,ref_data)
            embed=re.compile("var url = '(.+?)'").findall(html)[0]
            ref_data = {'Referer': url_frame,'User-Agent':user_agent}
            html= abrir_url_tommy(embed,ref_data)
            swf=re.compile("SWFObject\('(.+?)'").findall(html)[0].replace('../','')
            rtmp=re.compile("'streamer', '(.+?)'").findall(html)[0].replace('redirect','live')
            filep=re.compile("'file', '(.+?)'").findall(html)[0]
            rtmp=rtmp.replace('live','redirect')
            streamurl=rtmp + ' playPath=' + filep + ' swfUrl=http://castfree.net' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=' + embed
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('castto.me',link):
            marcador="Catcher: castto.me"; print marcador
            castamp=re.compile('fid="(.+?)".+?</script>').findall(link)
            for chname in castamp:
                embed='http://static.castto.me/embed.php?channel='+chname+'&vw=650&vh=500&domain='+url_frame
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                if re.search('Channel does not exist',html):
                    if activado==False: mensagemok('TV Portuguesa','Stream está offline.')
                    return
                swf=re.compile("SWFObject.+?'(.+?)'").findall(html)[0]
                filelocation=re.compile("so.addVariable.+?file.+?'(.+?)'").findall(html)[0]
                rtmpendereco=re.compile("so.addVariable.+?streamer.+?'(.+?)'").findall(html)[0]
                streamurl=rtmpendereco + ' playPath=' + filelocation + ' swfUrl=' + swf + ' live=true timeout=15 swfVfy=1 token=#ed%h0#w@1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('clubbingtv.live',link):
            marcador="Catcher: clubbingtv oficial"; print marcador
            rtmp=re.compile('file: "(.+?)"').findall(link)[0].replace('flv:','//')
            swf=re.compile('flashplayer: "(.+?)"').findall(link)[0]
            streamurl=rtmp + ' swfUrl=' + swf + ' live=true timeout=15 pageUrl=' + url_frame
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('ChelTV',link) or re.search('visionip',link):
            marcador="Catcher: cheltv"; print marcador
            chelsea=re.compile("file=(.+?).flv&streamer=(.+?)&").findall(link)
            try:swf=re.compile('flashvars=.+?src="(.+?)" type="application/x-shockwave-flash">').findall(link)[0]
            except:swf=re.compile("src='(.+?)' allowfullscreen=").findall(link)[0]
            streamurl=chelsea[0][1] + ' playPath=' + chelsea[0][0] + ' swfUrl=' + swf + ' live=true pageUrl=http://www.casadossegredos.tv'
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('www.dcast.tv',link):
            marcador="Catcher: dcast"; print marcador
            dcastfid=re.compile('<script type="text/javascript">fid="([^"]+)";').findall(link)[0]
            embed ="http://www.dcast.tv/embed.php?u="+dcastfid+"&vw=600&vh=450"
            ref_data = {'Referer': url_frame,'User-Agent':user_agent}
            html= abrir_url_tommy(embed,ref_data)
            streamurl='rtmpe://strm.dcast.tv/redirect playPath=' + dcastfid + ' swfUrl=http://www.dcast.tv/player/player.swf live=true timeout=15 pageUrl=http://www.dcast.tv/embed.php'
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('cdn.livestation',link):
            marcador="Catcher: livestation"; print marcador
            hdmi=re.compile('src="([^"]+?).swf.+?streamer=(.+?)&file=(.+?)&').findall(link)[0]
            streamurl=hdmi[1] + ' playPath=' + hdmi[2] + ' swfUrl=' + hdmi[0] + '.swf live=true swfVfy=true pageUrl=http://www.livestation.com'
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('direct-stream', link):
            marcador="Catcher: direct-stream"; print marcador
            stream4u=re.compile('fid="(.+?)";.+?></script>').findall(link)
            for chid in stream4u:
                embed='http://direct-stream.org/embednews.php?c='+chid
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data).encode('latin-1','ignore')
                rtmp=re.compile('file: "(.+?)"').findall(html)[0]
                playpath=''.join(rtmp.split('/')[-1:])
                streamurl=rtmp + ' playPath=' + playpath + ' swfUrl=http://direct-stream.org/jwplayer.flash.swf live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('elahmad.com',url_frame):
            marcador="Catcher: elahmad.com tvtuga stolen tvi"; print marcador
            streamurl=url_frame.replace('http://www.elahmad.com/tv/jwplayer.php?file=','')
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('ezcast', link):
            marcador="Catcher: ezcast"; print marcador
            ezcast=re.compile("channel='(.+?)',.+?</script>").findall(link)
            if not ezcast: ezcast=re.compile('src="/ezcast.tv.php.+?id=(.+?)" id="innerIframe"').findall(link)
            if not ezcast: ezcast=re.compile('channel="(.+?)",.+?</script>').findall(link)
            for chname in ezcast:
                embed='http://www.ezcast.tv/embedded/' + chname + '/1/555/435'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                if re.search("<small> Channel is domain protected. This channel can't be embedded on this domain name.</small>",html):
                    ref_data = {'Referer': 'http://cdn.zuuk.org','User-Agent':user_agent}
                    html= abrir_url_tommy(embed,ref_data)
                link=abrir_url('http://www.ezcast.tv:1935/loadbalancer')
                rtmpendereco=re.compile(".*redirect=([\.\d]+).*").findall(link)[0]
                swf=re.compile('SWFObject\("(.+?)"').findall(html)[0]
                idnum=re.compile("'FlashVars'.+?id=(.+?)&s=.+?&").findall(html)[0]
                chnum=re.compile("'FlashVars'.+?id=.+?&s=(.+?)&").findall(html)[0]
                streamurl='rtmp://' + rtmpendereco + '/live playPath=' + chnum + '?id=' + idnum + ' swfUrl=http://www.ezcast.tv' + swf + ' live=true conn=S:OK swfVfy=1 timeout=14 ccommand=iUsteJaSakamCarevataKerka;TRUE;TRUE pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('.f4m&', link):
            marcador="Catcher f4m file"; print marcador
            streamurl='http://' + clean(re.compile('src=http://(.+?).f4m&').findall(link)[0]) + '.f4m' #rtp1
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('fcast', link):
            marcador="Catcher: fcast"; print marcador
            fcast=re.compile("fid='(.+?)';.+?></script>").findall(link)
            if not fcast: fcast=re.compile("e-fcast.tv.php.+?fid=(.+?).flv").findall(link)
            for chname in fcast:
                embed='http://www.fcast.tv/embed.php?live=' + chname + '&vw=600&vh=400'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                swf=re.compile("SWFObject.+?'(.+?)'").findall(html)
                filelocation=re.compile("so.addVariable.+?file.+?'(.+?)'").findall(html)
                rtmpendereco=re.compile("so.addVariable.+?streamer.+?'(.+?)'").findall(html)
                streamurl=rtmpendereco[0] + ' playPath=' + filelocation[0] + ' swfUrl=' + swf[0] + ' live=true timeout=14 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('flashi', link):
            marcador="Catcher: flashi"; print marcador
            flashi=re.compile('fid="(.+?)";.+?></script>').findall(link)
            for chname in flashi:
                embed='http://www.flashi.tv/embed.php?v=' + chname +'&vw=640&vh=490&typeplayer=0&domain=f1-tv.info'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                if re.search('This Channel is not Existed !',html):
                    if activado==False: mensagemok('TV Portuguesa','Stream indisponivel')
                    return
                swf=re.compile("new SWFObject.+?'(.+?)'").findall(html)[0]
                filename=re.compile("so.addVariable.+?'file'.+?'(.+?)'").findall(html)
                #rtmpendereco=re.compile("so.addVariable.+?'streamer'.+?'(.+?)'").findall(link)
                streamurl='rtmp://flashi.tv:1935/lb' + ' playPath=' + filename[0] + ' swfUrl=http://www.flashi.tv/' + swf + ' live=true timeout=15 swfVfy=true pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('flashstreaming.mobi',link):
            marcador="Catcher: flashstreaming.mobi"; print marcador
            flex=re.compile("channel='(.+?)',.+?></script>").findall(link)
            for chid in flex:
                js=re.compile('http://flashstreaming.mobi/(.+?).js').findall(link)[0]
                temp=abrir_url('http://flashstreaming.mobi/%s.js' % js)
                embed=re.compile("src=(.+?)'").findall(temp)[0]+chid+'&w=600&h=400'
                #embed='http://flashstreaming.mobi/embed/embed.php?channel='+chid+'&w=600&h=400'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                try:swf=re.compile("new SWFObject\('(.+?)'").findall(html)[0]
                except:swf=re.compile("src='(.+?)'").findall(html)[0]
                try:playp=re.compile('file=(.+?)&').findall(html)[0]
                except:playp=re.compile("'file', '(.+?)'").findall(html)[0]
                try:rtmp=re.compile('streamer=(.+?)&').findall(html)[0]
                except:rtmp=re.compile("'streamer', '(.+?)'").findall(html)[0]
                streamurl=rtmp + ' playPath=' + playp + ' swfUrl=' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('flashtv.co', link):
            marcador="Catcher: flashtv.co"; print marcador
            stream4u=re.compile("fid='(.+?)';.+?></script>").findall(link)
            for chid in stream4u:
                embed='http://www.flashtv.co/embed.php?live='+chid+'&vw=650&vh=400'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                swf=re.compile("SWFObject\('(.+?)'").findall(html)[0]
                rtmp=re.compile("'streamer','(.+?)'").findall(html)[0]
                streamurl=rtmp + ' playPath=' + chid + ' swfUrl=http://www.flashtv.co' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('flexstream', link):
            marcador="Catcher: flexstream"; print marcador
            flex=re.compile("file='(.+?)';.+?></script>").findall(link)
            for chid in flex:
                pass #ja nao existe
                #embed='http://flexstream.net/embed.php?file='+chid+'&width=650&height=400'
                #ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                #html= abrir_url_tommy(embed,ref_data)
                #rtmp=re.compile("file: '(.+?)'").findall(html)[0].replace(chid,'')
                #streamurl=rtmp + ' playPath=' + chid + ' swfUrl=http://p.jwpcdn.com/6/8/jwplayer.flash.swf live=true timeout=15 swfVfy=1 pageUrl=' + embed
                #comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('fxstream.biz', link):
            marcador="Catcher: fxstream.biz"; print marcador
            flex=re.compile("file='(.+?)';.+?></script>").findall(link)
            for chid in flex:
                embed='http://fxstream.biz/embed.php?file='+chid+'&width=650&height=400'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                rtmp=re.compile("file: '(.+?)'").findall(html)[0].replace(chid,'')
                token=re.compile('securetoken: "(.+?)"').findall(html)[0].replace(chid,'')
                streamurl=rtmp + ' playPath=' + chid + ' swfUrl=http://p.jwpcdn.com/6/11/jwplayer.flash.swf token='+token+' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)


        elif re.search('freebroadcast.pw', link):
            marcador="Catcher: freebroadcast.pw"; print marcador
            flive=re.compile("channel='(.+?)',.+?></script>").findall(link)
            for chid in flive:
                embed='http://freebroadcast.pw/embed/embed.php?n='+chid+'&w=650&h=400'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                swf=re.compile("SWFObject\('../(.+?)'").findall(html)[0]
                playp=re.compile("'file', '(.+?)'").findall(html)[0]
                rtmp=re.compile("'streamer', '(.+?)'").findall(html)[0]
                token=re.compile("'token', '(.+?)'").findall(html)[0]
                streamurl=rtmp + ' playPath=' + playp + ' swfUrl=http://freebroadcast.pw/' + swf + ' live=true token=' +token +' timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('freelivetv.tv', link):
            marcador="Catcher: freelivetv.tv"; print marcador
            flive=re.compile("channel='(.+?)',.+?></script>").findall(link)
            for chid in flive:
                embed='http://freelivetv.tv/embed/embed.php?channel='+chid+'&w=650&h=400'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                swf=re.compile("src='(.+?)'").findall(html)[0]
                playp=re.compile('file=(.+?)&').findall(html)[0]
                rtmp=re.compile('streamer=(.+?)&').findall(html)[0]
                streamurl=rtmp + ' playPath=' + playp + ' swfUrl=' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('freetvcast', link):
            marcador="Catcher: freetvcast"; print marcador
            cenas=re.compile('freetvcast.pw/(.+?)"').findall(link)[0]
            ref_data = {'Referer': url_frame,'User-Agent':user_agent}
            framesite='http://freetvcast.pw/' + cenas
            html= abrir_url_tommy(framesite,ref_data)
            embed=re.compile("var url = '(.+?)'").findall(html)[0]
            ref_data = {'Referer': url_frame,'User-Agent':user_agent}
            html= abrir_url_tommy(embed,ref_data)
            swf=re.compile("SWFObject\('(.+?)'").findall(html)[0].replace('../','')
            rtmp=re.compile("'streamer', '(.+?)'").findall(html)[0].replace('redirect','live')
            filep=re.compile("'file', '(.+?)'").findall(html)[0]
            streamurl=rtmp + ' playPath=' + filep + ' swfUrl=http://freetvcast.pw/' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=' + embed
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('goodcast.me', link):
            marcador="Catcher: goodcast.me"; print marcador
            stream4u=re.compile("id='(.+?)';.+?></script>").findall(link)
            for chid in stream4u:
                embed='http://goodcast.me/stream.php?id='+chid+'&width=650&height=450&stretching='
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                playpath=re.compile('file=(.+?)&').findall(html)[0]
                swf=re.compile('data="(.+?)"').findall(html)[0]
                rtmp=re.compile("streamer=(.+?)&").findall(html)[0]
                abrir_url('http://goodcast.me/stream.html?id=' + playpath)
                streamurl=rtmp + ' playPath=' + playpath + ' swfUrl=' + swf + ' token=Fo5_n0w?U.rA6l3-70w47ch live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('hdcast.tv',link):
            marcador="Catcher: hdcast.tv"; print marcador
            chid=re.compile('fid=(.+?)"').findall(link)[0]
            chid=chid.replace('.flv','')
            streamurl='rtmp://origin.hdcast.tv:1935/redirect/ playPath='+chid+' swfUrl=http://www.udemy.com/static/flash/player5.9.swf live=true timeout=15 swfVfy=1 pageUrl=http://www.hdcast.tv'
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('hdcaster.net', link):
            marcador="Catcher: hdcaster"; print marcador
            hdcaster=re.compile("<script type='text/javascript'>id='(.+?)'").findall(link)
            for chid in hdcaster:
                urltemp='rtmp://188.138.121.99/hdcaster playPath=' + chid + ' swfUrl=http://hdcaster.net/player.swf pageUrl=http://hdcaster.net/player.php?channel_id=101634&width=600&height=430'
                token = '%Xr8e(nKa@#.'
                streamurl=urltemp + ' token=' + token
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('hqstream.tv', link):
            marcador="Catcher: hqstream.tv"; print marcador
            hqst=re.compile("hqstream.tv.+?streampage=(.+?)&").findall(link)
            for chid in hqst:
                embed='http://hqstream.tv/player.php?streampage=' + chid
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                fp=int(re.compile('var f =\s*([^;]+)').findall(html)[0])
                ap=int(re.compile('var a =\s*([^;]+)').findall(html)[0])/fp
                bp=int(re.compile('var b =\s*([^;]+)').findall(html)[0])/fp
                cp=int(re.compile('var c =\s*([^;]+)').findall(html)[0])/fp
                dp=int(re.compile('var d =\s*([^;]+)').findall(html)[0])/fp
                vp=re.compile("var v_part =\s*'([^']+).*").findall(html)[0]

                streamurl='rtmp://%s.%s.%s.%s%s swfUrl=http://filo.hqstream.tv/jwp6/jwplayer.flash.swf live=1 timeout=15 swfVfy=1 pageUrl=%s' % (ap,bp,cp,dp,vp,embed)
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('icasthd', link):
            marcador="Catcher: icastHD"; print marcador
            icast=re.compile('fid="(.+?)";.+?></script>').findall(link)
            for chname in icast:
                embed='http://www.icasthd.tv/embed.php?v='+chname+'&vw=575&vh=390&domain=www.ihdsports.com'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                if re.search('This Channel is not Existed !',html):
                    if activado==False: mensagemok('TV Portuguesa','Stream indisponivel')
                    return
                swf=re.compile("'flashplayer': 'http://www.icasthd.tv//(.+?)'").findall(html)[0]
                filename=re.compile("'file': '(.+?)'").findall(html)[0]
                rtmpendereco=re.compile("'streamer': '(.+?)redirect3").findall(html)[0]
                app=re.compile("Ticket=(.+?)'").findall(html)[0]
                streamurl=rtmpendereco+ 'live app=live?f=' + app + ' playPath=' + filename + ' swfUrl=http://www.icasthd.tv/' + swf + ' live=1 timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('janjua',link):
            marcador="Catcher: janjua"; print marcador
            janj=re.compile("channel='(.+?)',.+?</script>").findall(link)
            if not janj: janj=re.compile('channel="(.+?)",.+?</script>').findall(link)
            for chname in janj:
                embed='http://www.janjua.tv/embedplayer/'+chname+'/1/650/500'
                ref_data = {'Connection': 'keep-alive','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                if re.search('Channel is domain protected.',html):
                    url_frame='http://www.janjua.tv/' + chname
                    ref_data = {'Connection': 'keep-alive','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Referer': url_frame,'User-Agent':user_agent}
                    html= abrir_url_tommy(embed,ref_data)
                swf=re.compile('SWFObject.+?"(.+?)",').findall(html)
                flashvars=re.compile("so.addParam.+?'FlashVars'.+?'(.+?);").findall(html)[0]
                flashvars=flashvars.replace("')","&nada").split('l=&')
                if flashvars[1]=='nada':
                    nocanal=re.compile("&s=(.+?)&").findall(flashvars[0])[0]
                    chid=re.compile("id=(.+?)&s=").findall(html)[0]
                else:
                    nocanal=re.compile("&s=(.+?)&nada").findall(flashvars[1])[0]
                    chid=re.compile("id=(.+?)&s=").findall(html)[1]
                nocanal=nocanal.replace('&','')
                link=abrir_url('http://www.janjua.tv:1935/loadbalancer')
                embed='http://www.janjua.tv/embedplayer/'+chname+'/1/650/500'
                ref_data = {'Connection': 'keep-alive','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Referer': url_frame,'User-Agent':user_agent}
                rtmpendereco=re.compile(".*redirect=([\.\d]+).*").findall(link)
                streamurl='rtmp://' + rtmpendereco[0] + '/live/ playPath=' + nocanal + '?id=' + chid + ' swfVfy=1 conn=S:OK live=true ccommand=soLagaDaSeStoriAga;FALSE swfUrl=http://www.janjua.tv' + swf[0] + ' ccommand=soLagaDaSeStoriAga;TRUE;TRUE pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('jwplayer:streamer',link):
            marcador="Catcher: jwplayer.streamer .xml"; print marcador
            rtmp=re.compile('<jwplayer:streamer>(.+?)</jwplayer:streamer>').findall(link)[0]
            try:
                filelocation=re.compile('<media:content bitrate=".+?" url="(.+?)" width=".+?"').findall(link)[0]
            except:
                filelocation= re.compile('<media:content url="(.+?)"').findall(link)[0]
                if re.search('TPAI.mp4',filelocation): url_frame='http://muntumedia.com/television/10-tpai'

            swf='http://www.tpai.tv/swf/jwplayer/player.swf'
            streamurl=rtmp + ' playPath=' + filelocation + ' swfUrl=' + swf + ' live=true pageUrl=' + url_frame
            comecarvideo(streamurl,nomecanal,True,zapping)


        elif re.search('longtail', link):
            marcador="Catcher: longtail"; print marcador
            longtail=re.compile("src='http://player.longtailvideo.com/player.swf' flashvars='file=(.+?)&streamer=(.+?)&").findall(link)
            if not longtail: longtail=re.compile('flashvars="file=(.+?)&streamer=(.+?)&').findall(link)
            if not longtail: longtail=re.compile('flashvars="file=(.+?)&.+?streamer=(.+?)&').findall(link)
            for chname,rtmp in longtail:
                chname=chname.replace('.flv','')
                streamurl=rtmp + ' playPath=' + chname + ' live=true swfUrl=http://player.longtailvideo.com/player.swf pageUrl=http://longtailvideo.com/'
                comecarvideo(streamurl,nomecanal,True,zapping)
            if not longtail:
                streamurl=re.compile('file: "(.+?)"').findall(link)[0]
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('hdm1.tv',link):
            marcador="Catcher: hdm1.tv"; print marcador
            hdmi=re.compile("fid='(.+?)';.+?></script>").findall(link)
            for chid in hdmi:
                embed='http://hdm1.tv/embed.php?live='+ chid +'&vw=600&vh=470'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                swf=re.compile("new SWFObject.+?'(.+?)'").findall(html)[0]
                filelocation=re.compile("so.addVariable.+?'file'.+?'(.+?)'").findall(html)
                rtmpendereco=re.compile("so.addVariable.+?'streamer'.+?'(.+?)'").findall(html)
                streamurl=rtmpendereco[0] + ' playPath=' + filelocation[0] + ' swfUrl=' + swf + ' live=true swfVfy=true pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)
            if not hdmi:
                hdmi=re.compile("src='(.+?).swf.+?file=(.+?)&streamer=(.+?)&autostart=true").findall(link)
                for swf,chid,rtmp in hdmi:
                    embed='http://hdm1.tv/embed.php?live='+ chid +'&vw=600&vh=470'
                    streamurl=rtmp + ' playPath=' + chid + ' swfUrl=' + swf + ' live=true swfVfy=true pageUrl=' + embed
                    comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('jimey',link):
            marcador="Catcher: jimey"; print marcador
            chname=re.compile("file='(.+?)';.+?</script>").findall(link)[0]
            embed= 'http://jimey.tv/player/embedplayer.php?channel=' + chname + '&width=640&height=490'
            ref_data = {'Referer': url_frame,'User-Agent':user_agent}
            html= abrir_url_tommy(embed,ref_data)
            rtmp=re.compile('&streamer=(.+?)/redirect').findall(html)[0]
            streamurl= rtmp + ' playPath='+chname + " token=zyklPSak>3';CyUt%)'ONp" + ' swfUrl=http://jimey.tv/player/fresh.swf live=true timeout=15 swfVfy=1 pageUrl=' + embed
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('jw-player.html?cid=',url_frame):
            marcador="Catcher: jwplay tvfree"; print marcador
            streamurl=url_frame.replace('http://tvfree.me/jw-player.html?cid=','')
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('jwlive',link) or re.search('jw-play',link):
            marcador="Catcher: jwlive"; print marcador
            endereco=TVCoresURL + re.compile('<br/><iframe src="(.+?)" id="innerIframe"').findall(link)[0]
            if re.search('tvfree.me/jw-player.html',endereco):
                streamurl=endereco.replace('http://tvfree.me/jw-player.html?cid=','')
            else:
                link=abrir_url(endereco)
                streamurl=re.compile('file: "(.+?)"').findall(link)[0]
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('livemeans', link):
            marcador="Catcher: livemeans"; print marcador
            stream=re.compile('<embed.+?src="(.+?)" flashvars="rtserver=(.+?)&livechannel').findall(link)[0]
            rtmp=stream[1].replace('rtserver','livenlin4?ovpfv=2.1.2').replace(':80',':1935').replace('rtmpt://','rtmp://')
            swf=stream[0]
            streamurl=rtmp + ' playPath=mp4:2livepln swfVfy=1 live=true swfUrl=' + swf + ' pageUrl=' + url_frame
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('liveflash', link):
            marcador="Catcher: liveflash"; print marcador
            flashtv=re.compile("channel='(.+?)',.+?></script>").findall(link)
            if not flashtv: flashtv=re.compile('channel="(.+?)".+?</script>').findall(link)
            if not flashtv: flashtv=re.compile('iframe src="/cc-liveflash.php.+?channel=(.+?)"').findall(link)
            if not flashtv: flashtv=re.compile("window.open.+?'/e-liveflash.tv.php.+?channel=(.+?)'").findall(link)
            if not flashtv: flashtv=re.compile("http://tvph.googlecode.com/svn/players/liveflash.html.+?ver=(.+?)'").findall(link)
            if not flashtv: flashtv=re.compile("pop-liveflash.php.+?get=(.+?)'").findall(link)

            for chname in flashtv:
                embed='http://www.liveflash.tv/embedplayer/' + chname + '/1/640/460'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                if re.search('Channel is domain protected.',html):
                    url_frame='http://www.liveflash.tv/' + chname
                    ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                    html= abrir_url_tommy(embed,ref_data)
                swf=re.compile('SWFObject.+?"(.+?)",').findall(html)
                flashvars=re.compile("so.addParam.+?'FlashVars'.+?'(.+?);").findall(html)[0]
                flashvars=flashvars.replace("')","&nada").split('l=&')
                if flashvars[1]=='nada':
                    nocanal=re.compile("&s=(.+?)&").findall(flashvars[0])[0]
                    chid=re.compile("id=(.+?)&s=").findall(html)[0]
                else:
                    nocanal=re.compile("&s=(.+?)&nada").findall(flashvars[1])[0]
                    chid=re.compile("id=(.+?)&s=").findall(html)[1]
                nocanal=nocanal.replace('&','')
                link=abrir_url('http://www.liveflash.tv:1935/loadbalancer')
                rtmpendereco=re.compile(".*redirect=([\.\d]+).*").findall(link)
                streamurl='rtmp://' + rtmpendereco[0] + '/stream/ playPath=' + nocanal + '?id=' + chid + ' swfVfy=1 conn=S:OK live=true swfUrl=http://www.liveflash.tv' + swf[0] + ' ccommand=kaskatijaEkonomista;TRUE;TRUE pageUrl=' + embed
                #print streamurl
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('livestreamtv', link):
            marcador="Catcher: livestreamtv"; print marcador
            flex=re.compile("file='(.+?)';.+?></script>").findall(link)
            for chid in flex:
                embed='http://livestreamtv.biz/globo.php?file='+chid+'&width=650&height=400'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                rtmp=re.compile('var streamer="(.+?)"').findall(html)[0]#.replace('redirect','live')
                playpath=re.compile("'file': '(.+?)'").findall(html)[0]
                swf=re.compile('var myPlayer="(.+?)"').findall(html)[0]
                streamurl=rtmp + ' playPath=' + playpath + ' swfUrl=http://livestreamtv.biz'+swf+' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)


        #elif re.search('livestream', link):
        #    marcador="Catcher: livestream"; print marcador
        #    livestream=re.compile("videoborda.+?channel=(.+?)&").findall(link)
        #    for chname in livestream:
        #        streamurl='rtmp://extondemand.livestream.com/ondemand playPath=trans/dv04/mogulus-user-files/ch'+chname+'/2009/07/21/1beb397f-f555-4380-a8ce-c68189008b89 live=true swfVfy=1 swfUrl=http://cdn.livestream.com/chromelessPlayer/v21/playerapi.swf pageUrl=http://cdn.livestream.com/embed/' + chname + '?layout=4&amp;autoplay=true'
        #        comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('master_tv', link):
            marcador="Catcher: mastertv"; print marcador
            mastertv=re.compile('src=".+?fid=(.+?)" name="frame"').findall(link)[0].replace('animax','disneyjr')
            descobrirresolver('http://tv-msn.com/' + mastertv + '.html', nomecanal,False,False,nomeserver)

        elif re.search('megatvhd',url_frame):
            marcador="Catcher: megatvhd.tv"; print marcador
            chid=re.compile('liveedge/(.+?)"').findall(link)[0]
            embed='http://megatvhd.tv/ch.php?id='+chid
            link=abrir_url(embed)
            rtmp=re.compile('file: "(.+?)"').findall(link)[0]
            rtmp=rtmp.replace('/'+chid,'')
            streamurl=rtmp + ' playPath='+chid + ' live=true swfUrl=http://player.longtailvideo.com/player.swf pageUrl='+embed
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('megom', link):
            marcador="Catcher: megom.tv"; print marcador
            megom=re.compile('HEIGHT=432 SRC="http://distro.megom.tv/player-inside.php.+?id=(.+?)&width=768&height=432"></IFRAME>').findall(link)
            for chname in megom:
                embed='http://distro.megom.tv/player-inside.php?id='+chname+'&width=768&height=432'
                link=abrir_url(embed)
                swf=re.compile(".*'flashplayer':\s*'([^']+)'.*").findall(link)[0]
                streamer=re.compile("'streamer': '(.+?)',").findall(link)[0]
                streamer=streamer.replace('live.megom.tv','37.221.172.85')
                streamurl=streamer + ' playPath=' + chname + ' swfVfy=1 swfUrl=' + swf + ' live=true pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('micast', link):
            marcador="Catcher: micast"; print marcador
            baseurl='http://micast.tv/chn.php?ch='
            micast=re.compile('micast.tv:1935/live/(.+?)/').findall(link)
            if not micast: micast=re.compile('ca="(.+?)".+?></script>').findall(link)
            if not micast: micast=re.compile('setTimeout.+?"window.open.+?' + "'http://micast.tv/gen.php.+?ch=(.+?)',").findall(link)
            if not micast: micast=re.compile('src="http://micast.tv/gen5.php.+?ch=(.+?)&amp;"').findall(link)
            if not micast: micast=re.compile('src="http://micast.tv/chn.php.+?ch=(.+?)"').findall(link)
            if not micast:
                if re.search('http://micast.tv/gens2.php',url_frame):
                    micast=[]
                    micast.append(url_frame.replace('http://micast.tv/gens2.php?ch=',''))
                    baseurl='http://micast.tv/gens2.php?ch='

            for chname in micast:
                #embed=redirect(baseurl+chname)
                embed= redirect('http://micast.tv/gens2.php?ch=cocoeranheta')
                link=abrir_url(embed)
                if re.search('refresh',link):
                    chname=re.compile('refresh" content="0; url=http://micast.tv/gen.php.+?ch=(.+?)"').findall(link)[0]
                    link=abrir_url('http://micast.tv/gen5.php?ch='+chname)
                try:
                    final=re.compile('file=(.+?)&amp;streamer=(.+?)&amp').findall(link)[0]
                    streamurl=final[1] + ' playPath=' + final[0] + ' swfUrl=http://files.mica.st/player.swf live=true timeout=15 swfVfy=1 pageUrl=http://micast.tv/gen.php?ch='+final[0]
                except:
                    rtmp=re.compile('file: "(.+?),').findall(link)[0]
                    rtmp=rtmp.split('/')
                    rtmp[2]=rtmp[2] + ':443'
                    rtmp='/'.join(rtmp)
                    chid=re.compile('/liveedge/(.+?)"').findall(rtmp)[0]
                    chidplay=chid.replace('.flv','')
                    rtmp=rtmp.replace(chid+'"','')
                    streamurl=rtmp + ' playPath=' + chname + ' swfUrl=http://micast.tv/jwplayer/jwplayer.flash.swf live=true timeout=15 swfVfy=1 pageUrl=' + embed

                comecarvideo(streamurl,nomecanal,True,zapping)
            if not micast:
                try:
                    micast=re.compile('<iframe src="(.+?)" id="innerIframe"').findall(link)[0]
                    link=abrir_url(TVCoresURL + micast)
                    if re.search('privatecdn',link):
                        descobrirresolver(url_frame,nomecanal,link,zapping,nomeserver)
                    else:
                        micast=re.compile('//(.+?).micast.tv/').findall(link)[0]
                        linkfinal='http://' + micast+  '.micast.tv'
                        link=abrir_url(linkfinal)
                        final=re.compile('file=(.+?)&amp;streamer=(.+?)&amp').findall(link)[0]
                        #if not final: final=re.compile("file=(.+?)&streamer=(.+?)'").findall(link)[0]
                        streamurl=final[1] + ' playPath=' + final[0] + ' swfUrl=http://files.mica.st/player.swf live=true timeout=15 swfVfy=1 pageUrl=http://micast.tv/gen.php?ch='+final[0]
                        comecarvideo(streamurl,nomecanal,True,zapping)
                except: pass

        elif re.search('mips', link):
            marcador="Catcher: mips"; print marcador
            mips=re.compile("channel='(.+?)',.+?></script>").findall(link)
            if not mips: mips=re.compile('channel="(.+?)",.+?></script>').findall(link)
            if not mips: mips=re.compile('<iframe src="/mips.tv.php.+?fid=(.+?)" id="innerIframe"').findall(link)
            if not mips: mips=re.compile("pop-mips.php\?get=(.+?)'").findall(link)
            for chname in mips:
                embed='http://www.mips.tv/embedplayer/' + chname + '/1/500/400'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                if re.search("The requested channel can't embedded on this domain name.",html):
                    source='http://www.mips.tv/' + chname
                    ref_data = {'Referer': source,'User-Agent':user_agent}
                    html= abrir_url_tommy(embed,ref_data)
                swf=re.compile('SWFObject.+?"(.+?)",').findall(html)[0]
                flashvars=re.compile("so.addParam.+?'FlashVars'.+?'(.+?);").findall(html)[0]
                flashvars=flashvars.replace("')","&nada").split('l=&')
                if flashvars[1]=='nada':
                    nocanal=re.compile("&s=(.+?)&e=").findall(flashvars[0])[0]
                    chid=re.compile("id=(.+?)&s=").findall(html)[0]
                else:
                    nocanal=re.compile("&s=(.+?)&nada").findall(flashvars[1])[0]
                    chid=re.compile("id=(.+?)&s=").findall(html)[1]
                nocanal=nocanal.replace('&','')
                link=abrir_url('http://www.mips.tv:1935/loadbalancer')
                rtmpendereco=re.compile(".*redirect=([\.\d]+).*").findall(link)[0]
                streamurl='rtmp://' + rtmpendereco + '/live/ playPath=' + nocanal + '?id=' + chid + ' swfVfy=1 live=true timeout=15 conn=S:OK swfUrl=http://www.mips.tv' + swf + ' ccommand=gaolVanusPobeleVoKosata;TRUE;TRUE pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('myhdcast',link):
            marcador="Catcher: myhdcast"; print marcador
            cast3d=re.compile('src="http://www.myhdcast.com/embed.php\?id=(.+?)&').findall(link)
            for chname in cast3d:
                embed='http://www.myhdcast.com/embedplayer.php?width=600&height=450&id='+chname+'&autoplay=true'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                tempomili=str(millis())
                urltoken=re.compile(""".*getJSON\("([^'"]+)".*""").findall(html)[0] + '&_='+ tempomili
                urltoken2= abrir_url_tommy(urltoken,ref_data)
                token=re.compile('"token":"(.+?)"').findall(urltoken2)[0]
                temp=re.compile("file: '(.+?)'").findall(html)[0]
                rtmp='/'.join(temp.split('/')[:-1])
                playpath=''.join(temp.split('/')[-1:])
                swf=re.compile('<script src="([^"]+?)/jwplayer.js"></script>').findall(html)[0] + '/jwplayer.flash.swf'
                streamurl=rtmp + ' playPath=' + playpath + ' swfUrl=' + swf + ' live=true token='+token+' timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('newsko.co.uk', link): ##nao esta
            marcador="Catcher: newsko.co.uk"; print marcador
            cast3d=re.compile('fid="(.+?)";.+?></script>').findall(link)
            for chname in cast3d:
                embed='http://www.newsko.co.uk/embed.php?channel=' + chname +'&vw=640&vh=385&domain=' + url_frame
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                swf=re.compile("new SWFObject\('(.+?)',").findall(html)
                filelocation=re.compile("'file','(.+?)'").findall(html)
                rtmpendereco=re.compile("'streamer','(.+?)'").findall(html)
                streamurl=rtmpendereco[0] + ' playPath=' + filelocation[0] + '?id=' + ' swfUrl=' + swf[0] + ' live=true timeout=15 swfVfy=true pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('pt.euronews',link):
            marcador="Catcher: euronews pt"; print marcador
            import requests
            headers = {'User-Agent': user_agent}
            datac= {'action':'getHexaglobeUrl'}
            urlrequest='http://pt.euronews' + re.compile('src="http://pt.euronews(.+?)"').findall(link)[0]
            r = requests.post(urlrequest, data=datac,headers=headers)
            headers = {'User-Agent': user_agent,'Referer':urlrequest}
            r = requests.get(r.text, headers=headers)
            if re.search('"status":"ok"',r.text):
                streamurl=re.compile('"pt":{"hls":"(.+?)"').findall(r.text)[0].replace('\\','')
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('privatecdn',link):
            marcador="Catcher: privatecdn"; print marcador
            privatecdn=re.compile('<script type="text/javascript">id="(.+?)"').findall(link)
            for chid in privatecdn:
                embed='http://privatecdn.tv/ch.php?id='+chid
                link=abrir_url(embed)
                rtmp=re.compile('file: "(.+?)"').findall(link)[0]
                rtmp=rtmp.replace('/'+chid,'')
                streamurl=rtmp + ' playPath='+chid + ' live=true swfUrl=http://player.longtailvideo.com/player.swf pageUrl='+embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('putlive', link):
            marcador="Catcher: putlive"; print marcador
            putlivein=re.compile("<iframe.+?src='.+?.swf.+?file=(.+?)&.+?'.+?></iframe>").findall(link)
            if not putlivein: putlivein=re.compile("file='(.+?)'.+?</script>").findall(link)
            if not putlivein: putlivein=re.compile('src="http://www.putlive.in/e/(.+?)"></iframe>').findall(link)
            for chname in putlivein:
                streamurl='rtmpe://199.195.199.172:443/liveedge2/ playPath=' + chname + ' swfUrl=http://www.megacast.io/player59.swf live=true timeout=15 swfVfy=1 pageUrl=http://putlive.in/'
                comecarvideo(streamurl,nomecanal,True,zapping)

        ##livesoccerhd
        elif re.search('src="http://cdn.gosporttv.com',link):
            marcador="Catcher: livesoccerhd stolen sptvhd"; print marcador
            ups=re.compile('<iframe.+?src="(.+?)"').findall(link)[0]
            descobrirresolver(ups,nomecanal,False,zapping,nomeserver)

        elif re.search('ptcanal', link):
            marcador="Catcher: ptcanal"; print marcador

            try:
                link=link.replace('content="setTimeout,','<p><script language="JavaScript">setTimeout')
                #descobrirresolver(url_frame,nomecanal,link,zapping,nomeserver)
                ptcanal=re.compile('<p><a href="(.+?)" onclick="window.open').findall(link)[0]
            except:
                try:ptcanal=re.compile('<p><iframe src="(.+?)"').findall(link)[0]
                except:ptcanal=re.compile("""setTimeout\("window.open\('([^"]+?)'""").findall(link)[0]

            descobrirresolver(ptcanal,nomecanal,False,zapping,nomeserver)

        elif re.search('RTP Play - RTP</title>',link):
            marcador="Catcher: RTP Play"; print marcador
            match=re.compile('\"file\": \"(.+?)\",\"application\": \"(.+?)\",\"streamer\": \"(.+?)\"').findall(link)
            temp = ['rtmp://' + match[0][2] +'/' + match[0][1] + '/' + match[0][0] + ' swfUrl=' + RTPURL + '/play/player.swf live=true timeout=15']
            temp.append(re.compile('\"smil\":\"(.+?)\"').findall(link)[0])
            if activado==True: opcao=True
            else:opcao= xbmcgui.Dialog().yesno("TV Portuguesa", "Escolha um stream da lista dos disponiveis.", "", "","Stream Extra", 'Stream Principal')
            if opcao: streamurl=temp[0]
            else: streamurl= redirect(temp[1])
            comecarvideo(streamurl, nomecanal,True,zapping)

        elif re.search('rtps',link):
            marcador="Catcher: rtps"; print marcador
            ficheiro=re.compile("file='(.+?).flv'.+?</script>").findall(link)[0]
            streamurl='rtmp://ec21.rtp.pt/livetv/ playPath=' + ficheiro + ' swfUrl=http://museu.rtp.pt/app/templates/templates/swf/pluginplayer.swf live=true timeout=15 pageUrl=http://www.rtp.pt/'
            comecarvideo(streamurl, nomecanal,True,zapping)

        elif re.search('h2e.rtp.pt',link) or re.search('h2g2.rtp.pt',link) or re.search('.rtp.pt',link) or re.search('provider=adaptiveProvider.swf',link) or re.search('file=rtp1',link):
            marcador="Catcher: rtp.pt"; print marcador
            link=link.replace('\\','').replace('">',"'>")
            if re.search('<strong><u>Clique para ver a ',link):
                urlredirect=re.compile("popup\('(.+?)'\)").findall(link)[0]
                descobrirresolver(urlredirect,nomecanal,False,zapping,nomeserver)
                return
            try:streamurl=re.compile("cid=(.+?).m3u8").findall(link)[0] + '.m3u8'
            except:
                try:
                    streamurl=re.compile("file=(.+?).m3u8(.+?)&").findall(link)[0]
                    streamurl='.m3u8'.join(streamurl)
                    streamurl=streamurl.replace('&abouttext=TV ZUNE PLAYER 2013','')
                except:
                    try:streamurl=re.compile("file=(.+?).m3u8").findall(link)[0] + '.m3u8'
                    except:
                        try:
                            rtmp=re.compile('streamer=(.+?)&').findall(link)[0]
                            filep=re.compile('file=(.+?)&').findall(link)[0]
                            try:swf=re.compile(" data='(.+?).swf\?").findall(link)[0] + '.swf'
                            except:swf=re.compile('src="(.+?)"').findall(link)[0]

                            streamurl=rtmp + ' playPath=' + filep + ' swfUrl=' + swf + ' swfVfy=1 live=1 pageUrl=http://tvzune.tv/'
                        except:
                            #embed=re.compile('<iframe src="/flashmedia.php\?channel=(.+?)" id="innerIframe"').findall(link)[0]
                            #ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                            #embed=TVCoresURL + '/flashmedia.php?channel=' + embed

                            #html= urllib.unquote(abrir_url_tommy(embed,ref_data)).replace('//-->','.rtp.pt')
                            #descobrirresolver(embed,nomecanal,html,zapping,nomeserver)
                            streamurl=url_frame.replace('http://tvfree.me/jw-player.html?cid=','')
                            #comecarvideo(streamurl,nomecanal,True,zapping)
                            #return
            #streamurl='rtmp://ec21.rtp.pt/livetv/ playPath=' + ficheiro + ' swfUrl=http://museu.rtp.pt/app/templates/templates/swf/pluginplayer.swf live=true timeout=15 pageUrl=http://www.rtp.pt/'
            comecarvideo(streamurl , nomecanal,True,zapping)

        elif re.search('meocanaltv.com/embed',link) or re.search('http://ow.ly/Fv4mL',link): #tvgente/tvdesporto
            marcador="Catcher: stolen meocanaltv from tvgente"; print marcador
            if re.search('<script type="text/javascript"> cid="',link): chid=re.compile('cid="(.+?)";.+?</script>').findall(link)[0]
            else: chid=re.compile('src="http://www.meocanaltv.com/embed/(.+?).php').findall(link)[0]
            meotv='http://www.meocanaltv.com/embed/' + chid  + '.php'
            ref_data = {'Referer': url_frame,'User-Agent':user_agent}
            html= abrir_url_tommy(meotv,ref_data)
            if re.search('embed.js',html):
                html+=abrir_url_tommy(re.compile('src="([^"]+?)embed.js"').findall(html)[0] + 'embed.js',ref_data).decode('string-escape')
            descobrirresolver(meotv,nomecanal,html,zapping,nomeserver)

        elif re.search('=myStream.sdp',link):
            marcador="Catcher: other rtp"; print marcador
            try:
                rtmpendereco=re.compile('streamer=(.+?)&').findall(link)[0]
                filepath=re.compile('file=(.+?)&').findall(link)[0]
                filepath=filepath.replace('.flv','')
            except:
                rtmpendereco=re.compile('file=(.+?)&').findall(link)[0]
                filepath=re.compile(';id=(.+?)&').findall(link)[0]

            swf="http://player.longtailvideo.com/player.swf"
            streamurl=rtmpendereco + ' playPath=' + filepath + ' swfUrl=' + swf + ' live=1 timeout=15 pageUrl=' + url_frame
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('pepestream.com',link) or re.search('src="http://www.livesportshd.eu/c',link) or re.search('cricfree.sx',link) or re.search('<p><iframe src="http://bit.ly/1lrVcOr"',link) or re.search('tugastream',link) or re.search('sicnoticias_sp.php',link) or re.search('verdirectotv.com/tv',link) or re.search('look-tvs.com',link):
            marcador="Catcher: stolen streams"; print marcador
            if re.search('pepestream.com',link): stolen='http://pepestream.com/' + re.compile('src="http://pepestream.com/(.+?)"').findall(link)[0]
            elif re.search('src="http://www.livesportshd.eu/c',link): stolen='http://www.livesportshd.eu/' + re.compile('src="http://www.livesportshd.eu/c(.+?)"').findall(link)[0]
            elif re.search('cricfree.sx',link): stolen='http://cricfree.sx/' + re.compile('src="http://cricfree.sx/(.+?)"').findall(link)[0]
            elif re.search('<p><iframe src="http://bit.ly/1lrVcOr"',link):stolen='http://bit.ly/1lrVcOr'
            elif re.search('tugastream',link): stolen='http://www.tugastream.com/' + re.compile('src=".+?tugastream.com/(.+?)".+?/iframe>').findall(link)[0]
            elif re.search('sicnoticias_sp.php',link): stolen = 'http://www.tugastream.com/sicnoticias_sp.php'
            elif re.search('verdirectotv.com/tv',link): stolen='http://verdirectotv.com/tv' + re.compile('src="http://verdirectotv.com/tv(.+?)">').findall(link)[0]
            elif re.search('look-tvs.com',link):stolen='http://www.look-tvs.com/' + re.compile('src="http://www.look-tvs.com/(.+?)"').findall(link)[0]
            else: iugsdaiusdagiuasd
            descobrirresolver(stolen,nomecanal,False,zapping,nomeserver)

        elif re.search('resharetv',link): #reshare tv
            marcador="Catcher: resharetv"; print marcador
            ref_data = {'Referer': 'http://resharetv.com','User-Agent':user_agent}
            html= abrir_url_tommy(url_frame,ref_data)
            html= clean(html)
            try:
                try: streamurl=re.compile(',  file: "(.+?)"').findall(html)[0]
                except: streamurl=re.compile('file: "(.+?)"').findall(html)[0]
            except:
                try:
                    swf=re.compile('<param name="movie" value="/(.+?)"></param>').findall(html)[0]
                    rtmp=re.compile('<param name="flashvars" value="src=http%3A%2F%2F(.+?)%2F_definst_%2F.+?%2Fmanifest.f4m&loop=true.+?">').findall(html)[0]
                    play=re.compile('_definst_%2F(.+?)%2Fmanifest.f4m&loop=true.+?">').findall(html)[0]
                except:
                    try:
                        swf=re.compile('src="(.+?)" type="application/x-shockwave-flash"').findall(html)[0]
                        rtmp=re.compile('streamer=(.+?)&amp').findall(html)[0]
                        play=re.compile('flashvars="file=(.+?).flv&').findall(html)[0]
                        streamurl='rtmp://' + urllib.unquote(rtmp) + ' playPath=' + play + ' live=true timeout=15 swfVfy=1 swfUrl=' + ResharetvURL + swf + ' pageUrl=' + ResharetvURL
                    except:
                        try:
                            frame=re.compile('<iframe.+?src="(.+?)">').findall(html)[0]
                            descobrirresolver(frame,nomecanal,False,zapping,nomeserver)
                            return
                        except:
                            if activado==False: mensagemok('TV Portuguesa','Não e possível carregar stream.')
                            return
            comecarvideo(streamurl, nomecanal,True,zapping)

        elif re.search('sharecast',link):
            marcador="Catcher: sharecast"; print marcador
            share=re.compile('src="http://sharecast.to/embed/(.+?)"></iframe>').findall(link)
            if not share: share=re.compile('src="http://sharecast.to/embed.php.+?ch=(.+?)"').findall(link)
            for chname in share:
                embed= 'http://sharecast.to/embed/' + chname
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                if re.search('Channel not found',html):
                    if activado==False: mensagemok('TV Portuguesa','Stream offline.')
                    return
                try:
                    playpath= re.compile('file: "(.+?)",').findall(html)[0]
                    rtmp= re.compile('streamer: "(.+?)",').findall(html)[0]
                    conteudo=rtmp + ' playPath=' + playpath
                except:
                    rtmp= re.compile('file: "(.+?)",').findall(html)[0]
                    conteudo=rtmp

                streamurl= conteudo + ' live=true pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('surfline',link):
            marcador="Catcher: surfline"; print marcador
            idcam=re.compile('spotid = (.+?),').findall(link)[0]
            streaminfo=abrir_url('http://api.surfline.com/v1/syndication/cam/'+idcam).replace('\\','')
            if re.search('"camStatus":"down"',streaminfo):
                if activado==False: mensagemok('TV Portuguesa','Stream está offline.')
                return
            streamurl=re.compile('"file":"(.+?)"').findall(streaminfo)[0]
            comecarvideo(streamurl,nomecanal,True,zapping)

        #elif re.search('p,a,c,k,e,r',link):
        #    marcador="Catcher: zuuk ruu.php"; print marcador
        #    link=link.replace('|','')
        #    tuga=re.compile('ruuphpnr(.+?)style').findall(link)[0]
        #    descobrirresolver("http://www.zuuk.net/ruu.php?nr=" + tuga,nomecanal,False,zapping,nomeserver)

        elif re.search('http://portalzuca.net',link):
            marcador="Catcher: portalzuca"; print marcador
            tuga='http://portalzuca.net/' + re.compile('src="http://portalzuca.net/(.+?)"').findall(link)[0]
            descobrirresolver(tuga,nomecanal,False,zapping,nomeserver)

        elif re.search('pontucanal.net/iframe',link):
            marcador="Catcher: pontucanal iframe"; print marcador
            embed='http://pontucanal.tv/iframe/' + re.compile('src="http://pontucanal.net/iframe/(.+?)\?W=').findall(link)[0]
            ref_data = {'Referer': url_frame,'User-Agent':user_agent}
            html= abrir_url_tommy(embed,ref_data)
            descobrirresolver(embed,nomecanal,html,zapping,nomeserver)

        elif re.search('sawlive', link):
            marcador="Catcher: sawlive"; print marcador
            saw=re.compile('src="http://sawlive.tv/embed/(.+?)">').findall(link)
            for chid in saw:
                embed='http://sawlive.tv/embed/'+chid
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                link= abrir_url_tommy(embed,ref_data)
                jsU = JsUnpackerV2()
                link = urllib.unquote(jsU.unpackAll(link).replace(";Tamrzar.push('",'').replace("')",''))
                cont=re.compile('src="(.+?)"').findall(link)[0]
                ref_data = {'Referer': embed,'User-Agent':user_agent}
                html= jsU.unpackAll(abrir_url_tommy(cont,ref_data))
                swf=re.compile("SWFObject\('(.+?)',").findall(html)[0]
                filep=re.compile("'file', '(.+?)'").findall(html)[0]
                try:rtmp=re.compile("'streamer', '(.+?)'").findall(html)[0]
                except:rtmp=''
                streamurl=rtmp + ' playPath=' + filep + ' swfUrl='+swf+' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('streamcasttv', link):
            marcador="Catcher: streamcasttv"; print marcador
            scast=re.compile("file='(.+?)'.+?</script>").findall(link)
            if not scast: scast=re.compile('<iframe src="/streamcasttv.php\?file=(.+?)" id="innerIframe"').findall(link)
            for chid in scast:
                embed='http://www.streamcasttv.biz/embed.php?file='+chid+'&width=650&height=400'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data).encode('ascii','ignore').decode('utf-8')
                swf='http://www.streamcasttv.biz/jwplayer/jwplayer.flash.swf'
                if re.search("src='http://streamcasttv.biz/embed/",html):
                    extra=True
                    chid=re.compile("file='(.+?)';.+?</script>").findall(html)[0]
                    ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                    embed='http://www.streamcasttv.biz/embed/21r.php?file='+chid+'&width=650&height=400'
                    html= abrir_url_tommy(embed,ref_data).encode('ascii','ignore').decode('utf-8')
                    swf='http://www.streamcasttv.biz/embed/jwplayer/jwplayer.flash.swf'
                else: extra=False

                rtmp=re.compile("file: '(.+?)'").findall(html)[0]
                if extra==True: chid=''.join((rtmp.split('/'))[-1:]).replace('.smil','')
                rtmp='/'.join((rtmp.split('/'))[:-1]) + '/'
                streamurl=rtmp + ' playPath=' + chid + ' swfUrl='+swf+' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('streamify', link):
            marcador="Catcher: streamify"; print marcador
            flive=re.compile('channel="(.+?)",.+?></script>').findall(link)
            for chid in flive:
                embed='http://www.streamify.tv/embedplayer/'+chid+'/1/650/400'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                if re.search('Channel is domain protected.',html):
                    url_frame='http://www.streamify.tv/' + chname
                    ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                    html= abrir_url_tommy(embed,ref_data)
                swf=re.compile('SWFObject.+?"(.+?)",').findall(html)
                flashvars=re.compile("so.addParam.+?'FlashVars'.+?'(.+?);").findall(html)[0]
                flashvars=flashvars.replace("')","&nada").split('l=&')
                if flashvars[1]=='nada':
                    nocanal=re.compile("&s=(.+?)&").findall(flashvars[0])[0]
                    chid=re.compile("id=(.+?)&s=").findall(html)[0]
                else:
                    nocanal=re.compile("&s=(.+?)&nada").findall(flashvars[1])[0]
                    chid=re.compile("id=(.+?)&s=").findall(html)[1]
                nocanal=nocanal.replace('&','')
                link=abrir_url('http://www.streamify.tv:1935/loadbalancer')
                rtmpendereco=re.compile(".*redirect=([\.\d]+).*").findall(link)[0]
                streamurl='rtmp://' + rtmpendereco + '/live/ playPath=' + nocanal + '?id=' + chid + ' swfVfy=1 conn=S:OK live=true swfUrl=http://www.streamify.tv' + swf[0] + ' ccommand=keGoVidishStambolSoseBardovci;TRUE;TRUE pageUrl=' + embed
                #lib
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('sapo.pt',link):
            marcador="Catcher: sapo.pt"; print marcador
            if re.search('sapo.pt',url_frame):
                print "Method 1 - Direct"
                try:
                    print "Method 1a - via stream"
                    videoid=re.compile('http://videos.sapo.pt/(.+?)&').findall(url_frame)[0]
                    streamlist=abrir_url('http://videos.sapo.pt/%s?all=1' % (videoid))
                except:
                    print "Method 1b - via beach"
                    embed=re.compile('file=(.+?)&').findall(link)[0]
                    streamlist=abrir_url('%s?all=1' % (embed))
                streamurl=re.compile('"hls":"(.+?)"').findall(streamlist)[0].replace('\\','')
                comecarvideo(streamurl,nomecanal,True,zapping)
            elif re.search('file=',link) and re.search('flashvars',link):
                print "Method 2 - Embed"
                embed=re.compile('file=(.+?)&').findall(link)[0]
                streamlist=abrir_url('%s?all=1' % (embed))
                streamurl=re.compile('"hls":"(.+?)"').findall(streamlist)[0].replace('\\','')
                if re.search('sicnoticias2',streamurl): streamurl=streamurl.replace('sicnoticias2','sicnoticias') #temp hack to avoid tugastream3 freeze
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('surftotal',link):
            marcador="Catcher: surftotal"; print marcador
            try:
                try:streamurl=re.compile("""<source src="([^"]+?)" type='rtmp/mp4'>""").findall(link)[0]
                except:streamurl=re.compile('<source src="([^"]+?)" type="application/x-mpegURL">').findall(link)[0]
                comecarvideo(streamurl,nomecanal,True,zapping)
            except:
                if activado==False: mensagemok('TV Portuguesa','Stream está offline.')
                return


        elif re.search('telewizja',link) or re.search('sapo.tv.php',link):
            marcador="Catcher: telewizja or sapo.tv"; print marcador
            codigo=re.compile('<br/><iframe src="(.+?)" id="innerIframe"').findall(link)[0]
            ref_data = {'Referer': url_frame,'User-Agent':user_agent}
            embed=TVCoresURL + codigo
            html= abrir_url_tommy(embed,ref_data)
            descobrirresolver(embed,nomecanal,html,zapping,nomeserver)

        elif re.search('televisaofutebol',link):
            marcador="Catcher: televisaofutebol"; print marcador
            link=link.replace('\\','')
            tuga=re.compile('src="http://www.televisaofutebol.com/(.+?)".+?/iframe>').findall(link)[0]
            embed='http://www.televisaofutebol.com/' + tuga
            ref_data = {'Referer': 'http://www.estadiofutebol.com','User-Agent':user_agent}
            html= abrir_url_tommy(embed,ref_data)
            descobrirresolver(embed,nomecanal,html,zapping,nomeserver)

        elif re.search('http://tinyurl.com/',link):
            marcador="Catcher: tinyurl obfuscate"; print marcador
            embed= redirect(url_frame)
            descobrirresolver(embed,nomecanal,False,zapping,nomeserver)

        elif re.search('tvgo.be',url_frame):
            marcador="Catcher: tvbgo.be"; print marcador
            streamurl=re.compile('<a class="my-button" href="(.+?)"').findall(link)[0].replace('playlist','chunks')# + '|User-Agent=' + urllib.quote('PS3Application libhttp/4.5.5-000 (CellOS)')#Mozilla%2F5.0%20(iPad%3B%20CPU%20OS%206_0%20like%20Mac%20OS%20X)%20AppleWebKit%2?F536.26%20(KHTML%2C%20like%20Gecko)%20Version%2F6.0%20Mobile%2F10A5355d%20Safari?%2F8536.25'
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('tvtuga.com/live47/hls.swf',link):
            marcador="Catcher: tvtuga hls stolen streams"; print marcador
            streamurl=re.compile('file=(.+?)&').findall(link)[0]
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('streamago',link):
            marcador="Catcher: streamago"; print marcador
            flive=re.compile('<iframe src="http://www.streamago.tv/iframe/(.+?)/"').findall(link)
            if not flive:
                if re.search('streamago.php?id=',url_frame):
                    flive=url_frame('http://tvfree.me/streamago.php?id=','')
            for chid in flive:
                embed= redirect('http://www.streamago.tv/iframe/'+chid)
                html=abrir_url(embed)
                if re.search('the page you requested cannot be found.',html):
                    if activado==False: mensagemok('TV Portuguesa','Stream está offline.')
                    return
                swf=re.compile('swfobject.embedSWF\("(.+?)",').findall(html)[0]
                fvars=re.compile('flashvars.xml = "(.+?)"').findall(html)[0]
                dados=abrir_url(fvars)
                playpath=re.compile('<titolo id="(.+?)">').findall(dados)[0]
                rtmp=re.compile('<path><\!\[CDATA\[(.+?)\]\]></path>').findall(dados)[0]
                streamurl=rtmp + ' playPath=' + playpath + ' swfVfy=1 live=true swfUrl=http://www.streamago.tv' + swf + ' pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('tvdesporto.com',link):
            marcador="Catcher: tvdesporto"; print marcador
            chid=re.compile('src="http://www.tvdesporto.com/(.+?).php').findall(link.replace('\\',''))[0]
            urlredirect='http://www.tvdesporto.com/' + chid  + '.php'
            ref_data = {'Referer': url_frame,'User-Agent':user_agent}
            html= abrir_url_tommy(urlredirect,ref_data)
            descobrirresolver(urlredirect,nomecanal,html,zapping,nomeserver)

        elif re.search('tv-msn',link):
            marcador="Catcher: tv-msn"; print marcador
            if re.search('cdnbr.biz',link):
                link=link.replace('<img border="0" src="','')
                url_frame=re.compile('src="(.+?)"').findall(link)[0]
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                link= abrir_url_tommy(url_frame,ref_data).encode('ascii','ignore')
                swf=re.compile("<param name='movie' value='(.+?)'>").findall(link)[0]
            else:
                swf=re.compile("src='(.+?)'").findall(link)[0]

            variaveis=re.compile("file=(.+?).flv&streamer=(.+?)&").findall(link)[0]
            streamurl=variaveis[1] + ' playPath=' + variaveis[0]  + ' swfUrl='+swf+' live=true timeout=15 swfVfy=1 pageUrl='+url_frame

            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('tvph.googlecode.com',link):
            marcador="Catcher: tvph google code"; print marcador
            if re.search('playeer.html',link):
                info=re.compile("cid=file=(.+?)&streamer=(.+?)'").findall(link)[0]
                rtmp=info[1]
                streamurl=rtmp + ' playPath='+info[0]+' swfUrl=http://www.tvzune.tv/jwplayer/jwplayer.flash.swf live=true pageUrl=' + url_frame
            else:
                streamurl=re.compile("cid=(.+?)'").findall(link)[0]
            comecarvideo(streamurl,nomecanal,True,zapping)


        elif re.search('TV ZUNE PLAYER 201',link):
            marcador="Catcher: player tvzune soft"; print marcador
            rtmp=re.compile('streamer=(.+?)&').findall(link)[0]
            filep=re.compile('file=(.+?)&').findall(link)[0]
            ref_data = {'User-Agent':''}
            url_frame=url_frame.replace('canais','privado')
            html= abrir_url_tommy(url_frame,ref_data)

            ref_data = {'Accept': '*/*','User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; Trident/7.0; .NET4.0E; .NET4.0C; InfoPath.3; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729)','Cookie': 'jm3x_unique_user=1','Host': 'www.tvzune.tv','Connection': 'Keep-Alive'}
            nada= re.compile('<iframe.+?src="(.+?)"').findall(limparcomentarioshtml(abrir_url_tommy(html,ref_data),html))[0]

            ref_data = {'Accept': 'image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*','User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; Trident/7.0; .NET4.0E; .NET4.0C; InfoPath.3; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729)','Host': 'fire.tvzune.org','Connection': 'Keep-Alive'}
            nada= abrir_url_tommy(nada,ref_data)

            swf=re.compile('src="(.+?)"').findall(link)[0]
            streamurl=rtmp + ' playPath=' + filep + ' swfUrl=' + swf + ' swfVfy=1 live=1 pageUrl=' + html
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('player_tvzune',link):
            marcador="Catcher: player tvzune"; print marcador
            yoyo412=re.compile(yoyo115 + ' "(.+?)"').findall(link)[0]
            yoyo721='/'.join((yoyo412.split('/'))[:-1])
            yoyo721='rtmp://premium2.tvzune.org:1935/live/'
            yoyo428=re.compile('src="(.+?)"').findall(link)[0]
            yoyo683=re.compile(yoyo265 + '(.+?)"').findall(abrir_url(yoyo428))[0]
            yoyo378='/'.join((yoyo428.split('/'))[:-1]) + '/' + yoyo683
            streamurl=yoyo721 + ' playPath=' + yoyo412.split('/')[-1] + ' swfUrl=' +yoyo378 +' live=true pageUrl=' + url_frame
            comecarvideo(streamurl,nomecanal,True,zapping)


        elif re.search('stream4u', link):
            marcador="Catcher: stream4u"; print marcador
            stream4u=re.compile('fid="(.+?)";.+?></script>').findall(link)
            for chid in stream4u:
                embed='http://www.stream4u.eu/embed.php?v='+chid+'&vw=650&vh=400&domain='+url_frame
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                swf=re.compile("'flashplayer': '(.+?)'").findall(html)[0]
                rtmp=re.compile("'streamer': '(.+?)'").findall(html)[0]
                streamurl=rtmp + ' playPath=' + chid + ' swfUrl=' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('<meta property="og:url" content="http://www.tvi.iol',link): #tvioficial
            marcador="Catcher: tvi oficial"; print marcador
            streamurl=re.compile('file: "(.+?)"').findall(link)[0]
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('ukcast.co', link):
            marcador="Catcher: ukcast.co"; print marcador
            stream4u=re.compile('ukcast.co/.+?u=(.+?)&').findall(link)
            for chid in stream4u:
                embed='http://ukcast.co/embed.php?u='+chid+'&vw=100%&vh=100%'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                rtmp=re.compile('var str = "(.+?)";').findall(html)[0].replace('cdn','strm')
                swf=re.compile('new SWFObject\("(.+?)"').findall(html)[0]
                streamurl=rtmp + ' playPath=' + chid + ' swfUrl=' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('up4free', link):
            marcador="Catcher: up4free"; print marcador
            stream4u=re.compile("id='(.+?)';.+?></script>").findall(link)
            for chid in stream4u:
                embed='http://up4free.com/stream.php?id='+chid+'&width=650&height=450&stretching='
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                descobrirresolver(embed,nomecanal,html,zapping,nomeserver)

        elif re.search('valeucara', link):
            marcador="Catcher: valeucara"; print marcador
            valeu=re.compile('<script type="text/javascript"> id="(.+?)";.+?></script>').findall(link)
            for chid in valeu:
                embed='http://www.valeucara.com/'+chid+'_s.php?width=650&height=400'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= limparcomentarioshtml(abrir_url_tommy(embed,ref_data),embed)
                if re.search('file: "',html):
                    streamurl=re.compile('file: "(.+?)"').findall(html)[0]
                    comecarvideo(streamurl,nomecanal,True,zapping)
                else: descobrirresolver(embed,nomecanal,html,zapping,nomeserver)


        elif re.search('veecast',link):
            marcador="Catcher: veecast"; print marcador
            valeu=re.compile('src="http://www.veecast.net/e/(.+?)">').findall(link)
            for chid in valeu:
                embed='http://www.veecast.net/e/'+chid + '?width=640&height=480'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= urllib.unquote(abrir_url_tommy(embed,ref_data))
                rtmp=re.compile('streamer=(.+?)&').findall(html)[0]
                filep=re.compile('file=(.+?)&').findall(html)[0]
                swf=re.compile('src="(.+?)" type="application/x-shockwave-flash"').findall(html)[0]
                streamurl=rtmp + ' playPath=' + filep + ' swfUrl=' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=' + url_frame
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('vercosasgratis', link):
            marcador="Catcher: vercosasgratis"; print marcador
            try:cenas=re.compile("""vercosasgratis.com/([^"]+?)'""").findall(link)[0]
            except:cenas=re.compile('vercosasgratis.com/([^"]+?)"').findall(link)[0]
            ref_data = {'Referer': url_frame,'User-Agent':user_agent}
            framesite='http://vercosasgratis.com/' + cenas
            html= abrir_url_tommy(framesite,ref_data)
            embed=re.compile("var url = '(.+?)'").findall(html)[0]
            ref_data = {'Referer': url_frame,'User-Agent':user_agent}
            html= abrir_url_tommy(embed,ref_data)
            swf=re.compile("SWFObject\('(.+?)'").findall(html)[0].replace('../','')
            rtmp=re.compile("'streamer', '(.+?)'").findall(html)[0]
            filep=re.compile("'file', '(.+?)'").findall(html)[0]
            streamurl=streamurl=rtmp + ' playPath=' + filep + ' swfUrl=http://vercosasgratis.com/' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=' + embed
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('veetle',url_frame) or re.search("src='http://veetle",link) or re.search('src="http://veetle',link):
            marcador="Catcher: veetle"; print marcador
            if activado==False:
                if selfAddon.getSetting("verif-veetle3") == "false":
                    ok = mensagemok('TV Portuguesa','Necessita de instalar o addon veetle.','Este irá ser instalado já de seguida.')
                    urlfusion='http://fightnight-xbmc.googlecode.com/svn/addons/fightnight/plugin.video.veetle/plugin.video.veetle-0.3.1.zip' #v2.3
                    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
                    lib=os.path.join(path, 'plugin.video.veetle.zip')
                    downloader(urlfusion,lib)
                    addonfolder = xbmc.translatePath(os.path.join('special://home/addons',''))
                    xbmc.sleep(2000)
                    dp = xbmcgui.DialogProgress()
                    #if dp.iscanceled(): dp.close()
                    dp.create("TV Portuguesa", "A instalar...")
                    try:
                        extract(lib,addonfolder,dp,type="all")
                        ok = mensagemok('TV Portuguesa','Veetle instalado / actualizado.','Necessita de reiniciar o XBMC.')
                        selfAddon.setSetting('verif-veetle3',value='true')
                    except:
                        ok = mensagemok('TV Portuguesa','Sem acesso para instalar Veetle. Instale o veetle','do repositório fightnight.','De seguida, active o Veetle nas definições do addon.')
                else:
                    ## PATCH SPTHD IN LSHD
                    if re.search('var urls = new Array',link):
                            framedupla=re.compile('new Array.+?"(.+?)".+?"(.+?)"').findall(link)[0]
                            if framedupla[0]==framedupla[1]: frame=framedupla[0]
                            else:
                                if activado==True: opcao=True
                                else:opcao= xbmcgui.Dialog().yesno("TV Portuguesa", "Escolha um stream da lista dos disponiveis.", "", "","Stream Extra", 'Stream Principal')
                                if opcao: frame=framedupla[0]
                                else: frame=framedupla[1]
                            descobrirresolver(frame, nomecanal,False,False,nomeserver)
                            return

                    try:idembed=re.compile('/index.php/widget/index/(.+?)/').findall(link)[0]
                    except: idembed=re.compile('/index.php/widget#(.+?)/true/16:').findall(link)[0]
                    print "ID embed: " + idembed
                    try:
                        chname=abrir_url('http://fightnightaddons2.96.lt/tools/veet.php?id=' + idembed)
                        chname=chname.replace(' ','')
                        if re.search('DOCTYPE HTML PUBLIC',chname):
                            if activado==False: mensagemok('TV Portuguesa','Erro a obter link do stream. Tenta novamente.')
                            return
                        print "ID final obtido pelo TvM."
                    except:
                        chname=abrir_url('http://fightnight-xbmc.googlecode.com/svn/veetle/sporttvhdid.txt')
                        print "ID final obtido pelo txt."
                    print "ID final: " + chname
                    link=abrir_url('http://veetle.com/index.php/channel/ajaxStreamLocation/'+chname+'/flash')
                    if re.search('"success":false',link):
                        if activado==False: mensagemok('TV Portuguesa','O stream está offline.')
                    else:
                        streamfile='plugin://plugin.video.veetle/?channel=' + chname
                        comecarvideo(streamfile,nomecanal,True,zapping)

        elif re.search('veemi', link):
            marcador="Catcher: veemi"; print marcador
            veemi=re.compile('fid="(.+?)";.+?></script>').findall(link)
            for chid in veemi:
                embed='http://www.veemi.com/embed.php?v='+chid+'&vw=650&vh=400&domain='+url_frame
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                swf=re.compile("SWFObject\('(.+?)'").findall(html)[0]
                rtmp=re.compile("'streamer', '(.+?)'").findall(html)[0]
                streamurl=rtmp + ' playPath=' + chid + ' swfUrl=http://www.veemi.com/' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)


        elif re.search('www.wcast', link):
            marcador="Catcher: wcast"; print marcador
            wcast=re.compile("fid='(.+?)';.+?></script>").findall(link)
            for chid in wcast:
                embed='http://www.wcast.tv/embed.php?u=' + chid+ '&vw=600&vh=470'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                swf='http://www.wcast.tv/player/player.swf'
                filelocation=re.compile("so.addVariable.+?'file'.+?'(.+?)'").findall(html)
                rtmpendereco=re.compile("so.addVariable.+?'streamer'.+?'(.+?)'").findall(html)
                streamurl=rtmpendereco[0] + ' playPath=' + filelocation[0] + ' swfUrl=' + swf + ' live=true swfVfy=true pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('ucaster', link):
            marcador="Catcher: ucaster"; print marcador
            ucaster=re.compile("channel='(.+?)',.+?></script>").findall(link)
            if not ucaster: ucaster=re.compile('flashvars="id=.+?&s=(.+?)&g=1&a=1&l=').findall(link)
            if not ucaster: ucaster=re.compile('src="/ucaster.eu.php.+?fid=(.+?)" id="innerIframe"').findall(link)
            if not ucaster: ucaster=re.compile('flashvars="id=.+?&amp;s=(.+?)&amp;g=1').findall(link)
            if not ucaster: ucaster=re.compile("flashvars='id=.+?&s=(.+?)&").findall(link)
            if not ucaster: ucaster=re.compile('flashvars="id=.+?id=.+?&amp;s=(.+?)&amp;g=1').findall(link)
            if not ucaster: ucaster=re.compile('channel="(.+?)".+?g="1"').findall(link)
            #if not ucaster:
                #mensagemok('TV Portuguesa','Stream não é o do site responsável','logo não é possível visualizar.')
            for chname in ucaster:
                embed='http://www.ucaster.eu/embedded/' + chname + '/1/600/430'
                try:
                    ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                    html= abrir_url_tommy(embed,ref_data)
                    if re.search("<small> Channel is domain protected. This channel can't be embedded on this domain name.</small>",html):
                        ref_data = {'Referer': 'http://cdn.zuuk.org','User-Agent':user_agent}
                        html= abrir_url_tommy(embed,ref_data)
                    swf=re.compile('SWFObject.+?"(.+?)",').findall(html)[0]
                    flashvars=re.compile("so.addParam.+?'FlashVars'.+?'(.+?);").findall(html)[0]
                    if re.search('&a=1&l=www.tvgente.eu',flashvars): flashvars=flashvars.replace("')","&nada").split('l=www.tvgente.eu&')
                    else: flashvars=flashvars.replace("')","&nada").split('l=&')
                    if flashvars[1]=='nada':
                        nocanal=re.compile("&s=(.+?)&").findall(flashvars[0])[0]
                        chid=re.compile("id=(.+?)&s=").findall(html)[0]
                    else:
                        nocanal=re.compile("&s=(.+?)&nada").findall(flashvars[1])[0]
                        chid=re.compile("id=(.+?)&s=").findall(html)[1]
                    nocanal=nocanal.replace('&','')
                except:
                    nocanal=chname
                    chid=re.compile("flashvars='id=(.+?)&s").findall(link)[0]
                    swf=re.compile("true' src='http://www.ucaster.eu(.+?)'").findall(link)[0]
                link=abrir_url('http://www.ucaster.eu:1935/loadbalancer')
                rtmpendereco=re.compile(".*redirect=([\.\d]+).*").findall(link)[0]
                streamurl='rtmp://' + rtmpendereco + '/live playPath=' + nocanal + '?id=' + chid + ' swfVfy=1 conn=S:OK live=true swfUrl=http://www.ucaster.eu' + swf + ' ccommand=vujkoMiLazarBarakovOdMonospitovo;TRUE;TRUE pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('xuuby',link): ##proteccao tvdez
            marcador="Catcher: xuuby"; print marcador
            xuuby=re.compile('chname="(.+?)".+?</script>').findall(link)
            if not xuuby: xuuby=re.compile('chname=(.+?)&').findall(link)
            for chname in xuuby:
                embed='http://www.xuuby.com/show.php?chname='+chname+'&width=555&height=555&a=1'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                html=urllib.unquote(html)
                rtmp=re.compile('streamer=(.+?)&').findall(html)[0]
                filep=re.compile('file=(.+?)&').findall(html)[0]
                swf=re.compile('src="([^"]+?)" type="application/x-shockwave-flash"').findall(html)[0]
                streamurl=rtmp + ' playPath=' + filep + ' live=true timeout=15 swfVfy=1 swfUrl=' + swf+' pageUrl=' + url_frame
                #http://www.xuuby.com/show2.php?chname=sica&width=555&height=555&a=1
                #streamurl=re.compile('file: "(.+?)"').findall(html)[0]
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('youtube.com/v',link):
            marcador="Catcher: youtube"; print marcador
            idvideo=re.compile('type="application/x-shockwave-flash" src="http://www.youtube.com/v/(.+?)&.+?"></object>').findall(link)[0]
            sources=[]
            import urlresolver
            embedvideo='http://www.youtube.com/watch?v=' + idvideo
            hosted_media = urlresolver.HostedMediaFile(url=embedvideo)
            sources.append(hosted_media)
            source = urlresolver.choose_source(sources)
            if source:
                streamurl=source.resolve()
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('yocast', link):
            marcador="Catcher: yocast"; print marcador
            stream4u=re.compile("fid='(.+?)';.+?></script>").findall(link)
            for chid in stream4u:
                embed='http://www.yocast.tv/embed.php?s='+chid+'&width=650&height=400&domain='+url_frame
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                swf=re.compile("'flashplayer': '(.+?)'").findall(html)[0]
                rtmp=re.compile("'streamer': '(.+?)'").findall(html)[0]
                streamurl=rtmp + ' playPath=' + chid + ' swfUrl=' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('youcloud', link):
            marcador="Catcher: youcloud"; print marcador
            hqst=re.compile("youcloud.tv/embed/(.+?)\?").findall(link)
            for chid in hqst:
                embed='http://youcloud.tv/player?streamname=' + chid
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                fp=int(re.compile('var f =\s*([^;]+)').findall(html)[0])
                ap=int(re.compile('var a =\s*([^;]+)').findall(html)[0])/fp
                bp=int(re.compile('var b =\s*([^;]+)').findall(html)[0])/fp
                cp=int(re.compile('var c =\s*([^;]+)').findall(html)[0])/fp
                dp=int(re.compile('var d =\s*([^;]+)').findall(html)[0])/fp
                vp=re.compile("var v_part =\s*'([^']+).*").findall(html)[0]

                streamurl='rtmp://%s.%s.%s.%s%s swfUrl=http://cdn.youcloud.tv/jwplayer.flash.swf live=1 timeout=15 swfVfy=1 pageUrl=%s' % (ap,bp,cp,dp,vp,embed)
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('yukons', link):
            marcador="Catcher: yukons"; print marcador
            yukons=re.compile('kuyo&file=(.+?)&').findall(link)
            if not yukons: yukons=re.compile("file='(.+?)'.+?</script>").findall(link)
            if not yukons: yukons=re.compile('channel="(.+?)".+?</script>').findall(link)
            if not yukons: yukons=re.compile('file=(.+?)&').findall(link)
            for chname in yukons:
                #idnumb='373337303331363236323737'
                idnumb='3733373033323632363237373331'
                ref_data = {'Host': 'yukons.net','Connection': 'keep-alive','Accept': '*/*','Referer': url_frame,'User-Agent':user_agent,'Cache-Control': 'max-age=0','Accept-Encoding': 'gzip,deflate,sdch'}
                import requests
                link= requests.get('http://yukons.net/yaem/' + idnumb,headers=ref_data)
                idfinal=re.compile("return '(.+?)'").findall(link.text)[0]
                token=re.compile('PHPSESSID=(.+?);').findall(link.headers['set-cookie'])[0]
                embed='http://yukons.net/embed/'+idnumb+'/'+idfinal+'/600/450'
                ref_data = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Referer': url_frame,'User-Agent':user_agent,'Host': 'yukons.net','Cache-Control': 'max-age=0','Accept-Encoding': 'gzip,deflate,sdch','Connection': 'keep-alive','Cookie':'PHPSESSID=' + token}
                html= requests.get(embed,headers=ref_data).text
                idrtmp=re.compile('FlashVars\|id\|(.+?)\|').findall(html)[0]
                pidrtmp=re.compile('\|pid\|\|(.+?)\|').findall(html)[0]
                swfrtmp=re.compile('SWFObject\|.+?\|\|\|(.+?)\|swf\|eplayer').findall(html)[0]
                ref_data = {'Referer': embed,'User-Agent':user_agent,'Host': 'yukons.net','Connection': 'keep-alive','Accept':'*/*','Accept-Encoding': 'gzip,deflate,sdch'}
                servertmp= abrir_url_tommy('http://yukons.net/srvload/'+ idrtmp,ref_data).replace('srv=','')
                streamurl='rtmp://' + servertmp + ':443/kuyo playPath=' + chname + '?id=' + idrtmp + '&pid=' + pidrtmp + ' swfUrl=http://yukons.net/'+swfrtmp + '.swf live=true conn=S:OK timeout=14 swfVfy=true ccommand=trxuwaaLahRKnaechb;TRUE;TRUE pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('wowcast.tv', link):
            marcador="Catcher: wowcast"; print marcador
            stream4u=re.compile('fid="(.+?)";.+?></script>').findall(link)
            for chid in stream4u:
                embed='http://www.wowcast.tv/embed.php?stream='+chid+'&vw=650&vh=400'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)

                swf=re.compile('SWFObject\("(.+?)"').findall(html)[0]
                rtmp=re.compile('"streamer", "(.+?)"').findall(html)[0]
                streamurl=rtmp + ' playPath=' + chid + ' swfUrl=' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('yycast', link):
            marcador="Catcher: yycast"; print marcador
            yycast=re.compile('fid="(.+?)";.+?</script><script type="text/javascript" src="http://www.yycast.com/javascript/embedPlayer.js"></script>').findall(link)
            if not yycast: yycast=re.compile("file='(.+?).flv'.+?</script>").findall(link)
            if not yycast: yycast=re.compile('fid="(.+?)".+?</script>').findall(link)
            if not yycast: yycast=re.compile('channel="(.+?)".+?</script>').findall(link)
            for chname in yycast:
                embed='http://yycast.com/embedded/'+ chname + '/1/555/435'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                link=abrir_url('http://yycast.com:1935/loadbalancer')
                rtmpendereco=re.compile(".*redirect=([\.\d]+).*").findall(link)[0]
                swf=re.compile('SWFObject.+?"(.+?)"').findall(html)[0]
                idnum=re.compile("'FlashVars', 'id=(.+?)&s=.+?'").findall(html)[0]
                chnum=re.compile("'FlashVars', 'id=.+?&s=(.+?)&").findall(html)[0]
                streamurl='rtmp://' + rtmpendereco + '/live/ playPath=' + chnum + '?id=' + idnum + ' swfVfy=1 timeout=15 conn=S:OK live=true ccommand=trajkoProkopiev;TRUE;TRUE swfUrl=http://yycast.com' + swf + ' pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('fa16bb1eb942c5c48ac3cd66aff4c32f2a015b1af198c14b88',link):
            marcador="Catcher: fa16bb hash"; print marcador
            stream4u=re.compile('id="(.+?)";.+?></script>').findall(link)
            for chid in stream4u:
                embed='http://fa16bb1eb942c5c48ac3cd66aff4c32f2a015b1af198c14b88.com/gen_s.php?id='+chid#+'&PageSpeed=noscript'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data).encode('latin-1','ignore')
                from resources.lib import unwise
                jsUW = unwise.JsUnwiser()
                if jsUW.containsWise(html):
                    html = jsUW.unwiseAll(html)
                temp=re.compile(",file:'(.+?)'").findall(html)[0]
                rtmp='/'.join(temp.split('/')[:-1])
                playpath=''.join(temp.split('/')[-1:])
                swf=re.compile('<script src="([^"]+?)/.+?html5.+?.js"></script>').findall(html)[0] + '/jwplayer.flash.swf'
                streamurl=rtmp + ' playPath=' + playpath + ' swfUrl=http://xuscacamusca.se/' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)


        elif re.search('xuscacamusca.se', link):
            marcador="Catcher: xuscacamusca.se"; print marcador
            stream4u=re.compile('id="(.+?)";.+?></script>').findall(link)
            for chid in stream4u:
                embed='http://xuscacamusca.se/?id='+chid+'&PageSpeed=noscript'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data).encode('latin-1','ignore')
                from resources.lib import unwise
                jsUW = unwise.JsUnwiser()
                if jsUW.containsWise(html):
                    html = jsUW.unwiseAll(html)
                temp=re.compile(",file:'(.+?)'").findall(html)[0]
                rtmp='/'.join(temp.split('/')[:-1])
                playpath=''.join(temp.split('/')[-1:])
                swf=re.compile('<script src="([^"]+?)/.+?html5.+?.js"></script>').findall(html)[0] + '/jwplayer.flash.swf'
                streamurl=rtmp + ' playPath=' + playpath + ' swfUrl=http://xuscacamusca.se/' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('mybeststream.xyz', link):
            marcador="Catcher: mybeststream.xyz"; print marcador
            stream4u=re.compile('id="(.+?)";.+?></script>').findall(link)
            for chid in stream4u:
                embed='http://mybeststream.xyz/?id='+chid+'&PageSpeed=noscript'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data).encode('latin-1','ignore')
                from resources.lib import unwise
                jsUW = unwise.JsUnwiser()
                if jsUW.containsWise(html):
                    html = jsUW.unwiseAll(html)
                temp=re.compile(",file:'(.+?)'").findall(html)[0]
                rtmp='/'.join(temp.split('/')[:-1])
                playpath=''.join(temp.split('/')[-1:])
                swf=re.compile('<script src="([^"]+?)/.+?html5.+?.js"></script>').findall(html)[0] + '/jwplayer.flash.swf'
                streamurl=rtmp + ' playPath=' + playpath + ' swfUrl=http://xuscacamusca.se/' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('pxstream', link):
            marcador="Catcher: pxstream"; print marcador
            stream4u=re.compile("file='(.+?)';.+?></script>").findall(link)
            for chid in stream4u:
                embed='http://pxstream.tv/embedrouter.php?file='+chid
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data).encode('latin-1','ignore')
                rtmp=re.compile('file: "(.+?)"').findall(html)[0]
                securetoken=re.compile('securetoken: "(.+?)"').findall(html)[0]
                playpath=''.join(rtmp.split('/')[-1:])
                streamurl=rtmp + ' playPath=' + playpath + ' swfUrl=http://pxstream.tv/jwplayer.flash.swf live=true timeout=15 token=' + securetoken + ' swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)


        elif re.search('zcast.us', link):
            marcador="Catcher: zcast"; print marcador
            zcast=re.compile('channel="(.+?)";.+?></script>').findall(link)
            for chname in zcast:
                embed='http://zcast.us/gen.php?ch=' + chname + '&width=700&height=480'
                streamurl='rtmp://gabon.zcast.us/liveedge' + ' playPath=' + url_frame + ' live=true timeout=15 swfVfy=1 swfUrl=http://player.zcast.us/player58.swf pageUrl=http://www.xuuby.com/'
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('zenex', link):
            marcador="Catcher: zenex"; print marcador
            zenex=re.compile("channel='(.+?)',.+?</script>").findall(link)
            for chname in zenex:
                embed='http://www.zenex.tv/embedplayer/' + chname + '/1/555/435'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                link=abrir_url('http://www.zenex.tv:1935/loadbalancer')
                rtmpendereco=re.compile(".*redirect=([\.\d]+).*").findall(link)[0]
                idnum=re.compile("'FlashVars'.+?id=(.+?)&s=.+?&").findall(html)[0]
                chnum=re.compile("'FlashVars'.+?id=.+?&s=(.+?)&").findall(html)[0]
                swf=re.compile('new SWFObject\("(.+?)"').findall(html)[0]
                streamurl='rtmp://' + rtmpendereco + '/zenex playPath=' + chnum + '?id=' + idnum + ' swfUrl=http://www.zenex.tv' + swf+ ' live=true conn=S:OK swfVfy=1 timeout=14 ccommand=goVideStambolSoseBardovci;TRUE;TRUE pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)


        elif re.search('src="http://www.dailymotion.com/embed',link) or re.search('"video_stream_mode":"',link):
            marcador="Catcher: dailymotion"; print marcador
            try:idvideo=re.compile('<iframe.+?src="http://www.dailymotion.com/embed(.+?)"').findall(link)[0]
            except:idvideo=re.compile('<meta name="twitter:player".+?/embed(.+?)"').findall(link)[0]
            sources=[]
            embedvideo='http://www.dailymotion.com/embed' + idvideo
            ref_data = {'Referer': url_frame,'User-Agent':user_agent}
            html= abrir_url_tommy(embedvideo,ref_data)
            if re.search('stream_live_hls_url',html):
                streamurl=re.compile('"stream_live_hls_url":"(.+?)"').findall(html)[0].replace('\\','')
            else:
                import urlresolver
                hosted_media = urlresolver.HostedMediaFile(url=embedvideo)
                sources.append(hosted_media)
                source = urlresolver.choose_source(sources)
                if source:
                    streamurl=source.resolve()
            comecarvideo(streamurl,nomecanal,True,zapping)


        else:
            marcador="Catcher: noserver" ; print marcador
            if activado==False:
                mensagemok('TV Portuguesa','Servidor não suportado')
                mensagemprogresso.close()
            else:
                try:debug.append(nomeserver + ' - ' + marcador)
                except: pass
    except Exception:
        if activado==False:
            mensagemprogresso.close()
            mensagemok('TV Portuguesa','Servidor não suportado.')
            (etype, value, traceback) = sys.exc_info()
            print etype
            print value
            print traceback
        else:
            try:debug.append(nomeserver + ' - ' + marcador)
            except: pass


def _descobrirresolver(url_frame,nomecanal,linkrecebido,zapping,nomeserver):
    mensagemprogresso.create('TV Portuguesa', 'A carregar stream. (' + nomeserver + ')','Por favor aguarde...')
    descobrirresolver(url_frame,nomecanal,linkrecebido,zapping,nomeserver)