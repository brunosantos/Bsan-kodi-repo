import re
import sys
from default import activado, mensagemprogresso, name, mensagemok, AltasEmocoesURL, TVCoresURL, SptveuURL, RedwebURL, \
    TVTugaURL, debug
from descobrirResolver import descobrirresolver
from requests import abrir_url_cookie, abrir_url_tommy, abrir_url
from resources.lib.daring import user_agent
from utils import clean, limparcomentarioshtml
from videoPlayer import comecarvideo

def pre_resolvers(titles,ligacao,index,nome,tamanho=0,zapping=False):
    marcador='A iniciar pre resolvers'
    try:
        sys.argv[2]=sys.argv[2]+ titles[index]
        if activado==True: mensagemprogresso.update(tamanho,'A criar lista. ' + nome+ ' ' + titles[index],'Por favor aguarde...')

        nomeserver=nome.replace('ç','c').replace('ã','a').replace('ó','o') + ' ' + titles[index]
        linkescolha=ligacao[index]
        if linkescolha:
            if re.search('api.torrent-tv.ru',linkescolha):
                marcador="Pre-catcher: torrent-tv"; print marcador
                if xbmc.getCondVisibility("System.HasAddon(plugin.video.p2p-streams)"):
                    link= clean(abrir_url_cookie(linkescolha))
                    if re.search('SPORTTV 1',nome): hname='Sport TV 1'
                    elif re.search('SPORTTV 2',nome): hname='Sport TV 2'
                    elif re.search('SPORTTV 3',nome): hname='Sport TV 3'
                    elif re.search('SPORTTV 4',nome): hname='Sport TV 4'
                    elif re.search('SPORTTV 5',nome): hname='Sport TV 5'
                    else: hname='non'
                    streamurl='plugin://plugin.video.p2p-streams/?url='+re.compile(hname+'.+?acestream://(.+?)#').findall(link)[0]+'&mode=1&name='+name
                    comecarvideo(streamurl,name,True,zapping)
                else:
                    if activado==False: mensagemok('TV Portuguesa','Precisa de instalar o addon p2p-streams!','Veja aqui como fazer:','http://bit.ly/p2p-instalar')

            elif re.search('estadiofutebol',linkescolha):
                marcador="Pre-catcher: tvdez"; print marcador
                link= abrir_url_cookie(linkescolha,forcedns=True)
                if re.search('televisaofutebol',link):
                    codigo=re.compile('<iframe src="http://www.televisaofutebol.com/([^"]+?)"').findall(link)[0]
                    embed='http://www.televisaofutebol.com/' + codigo
                    ref_data = {'Referer': 'http://www.estadiofutebol.com','User-Agent':user_agent}
                    html= abrir_url_tommy(embed,ref_data)
                    descobrirresolver(embed,nome,html,zapping,nomeserver)
                else:
                    descobrirresolver(linkescolha, nome,False,zapping,nomeserver)

            elif re.search('tugastream',linkescolha):
                marcador="Pre-catcher: tugastream"; print marcador
                link= abrir_url_cookie(linkescolha,forcedns=True)
                descobrirresolver(linkescolha, nome,False,zapping,nomeserver)

            elif re.search('altas-emocoes',linkescolha):
                marcador="Pre-catcher: altas emocoes /sporting"; print marcador
                link= abrir_url(linkescolha)
                frame=re.compile('<a href="/([^"]+?)" target="_blank">SPORTING TV.+?</td>').findall(link)[0]
                ref_data = {'Referer': linkescolha,'User-Agent':user_agent}
                frame1=AltasEmocoesURL + frame
                link= abrir_url_tommy(frame1,ref_data)
                frame2='http://www.livesportshd.eu/' + re.compile('src="http://www.livesportshd.eu/([^"]+?)"').findall(link)[0]
                ref_data = {'Referer': frame1,'User-Agent':user_agent}

                link= abrir_url_tommy(frame2,ref_data)
                #frame=re.compile("src='(.+?)'").findall(link)[0]
                #ref_data = {'Referer': frame2,'User-Agent':user_agent}
                #link= abrir_url_tommy(frame,ref_data)
                descobrirresolver(frame2, nome,link,zapping,nomeserver)

            elif re.search('verlatelegratis',linkescolha):
                marcador="Pre-catcher: verlatelegratis"; print marcador
                temporary=''
                link= abrir_url(linkescolha)
                listacanais=re.compile('<center><iframe.+?src="(.+?)"').findall(link)[0]
                link= abrir_url(listacanais)
                canais=re.compile("javascript:popUp\('(.+?)'").findall(link)
                for temp in canais:
                    if re.search('toro',temp) and re.search('Toros TV',nome):temporary=temp
                    if re.search('pesca',temp) and re.search('Caça e Pesca',nome) :temporary=temp
                if temporary!='':
                    if re.search('http://',temporary): baseurl=temporary
                    else:baseurl='/'.join(listacanais.split('/')[:-1]) + temporary
                    ref_data = {'Referer': listacanais,'User-Agent':user_agent}
                    link= abrir_url_tommy(baseurl,ref_data)
                    urlfinal=re.compile('<iframe.+?src="(.+?)"').findall(link)[0]
                    ref_data = {'Referer': baseurl,'User-Agent':user_agent}
                    link= abrir_url_tommy(urlfinal,ref_data)
                    descobrirresolver(urlfinal, nome,link,zapping,nomeserver)

            elif re.search('meocanaltv',linkescolha):
                marcador="Pre-catcher: meocanaltv"; print marcador
                embed=linkescolha.replace('canais.php?stream=','embed/') + '.php?width=600&height=450'
                ref_data = {'Referer': linkescolha,'User-Agent':user_agent}
                #html= abrir_url_tommy(embed,ref_data)
                from resources.lib import cloudflare
                html=cloudflare.webpage_request(embed)
                if re.search('embed.js',html):
                    html+= abrir_url_tommy(re.compile('src="([^"]+?)embed.js"').findall(html)[0] + 'embed.js',ref_data).decode('string-escape')
                descobrirresolver(embed,nome,html,zapping,nomeserver)

            elif re.search('tvfree',linkescolha):
                marcador="Pre-catcher: tv a cores"; print marcador
                ref_data = {'Referer': TVCoresURL,'User-Agent':user_agent}
                from resources.lib import cloudflare
                link=cloudflare.webpage_request(linkescolha)
                if re.search('antena.tvfree',link) or re.search('iframe id="player"',link):
                    marcador="Pre-catcher: tv a cores - antena"; print marcador
                    try:frame=re.compile('<iframe id="player"[^>]+?src="([^"]+?)"').findall(link)[0]
                    except:frame=re.compile('<iframe src="([^"]+?)" id="innerIframe"').findall(link)[0]
                    #if not re.search('antena.mytvfree',frame): frame= TVCoresURL + frame
                    ref_data = {'Referer': linkescolha,'User-Agent':user_agent}
                    #frame=frame.replace('http://mytvfree.mehttp://antena.mytvfree.me','http://antena.mytvfree.me/')
                    link= abrir_url_tommy(frame,ref_data)
                    descobrirresolver(frame, nome,link,zapping,nomeserver)

                elif re.search('src="/meocanal.php',link):
                    marcador="Pre-catcher: tv a cores - meocanal"; print marcador
                    tempId=re.compile('<iframe src="/meocanal.php\?id=([^"]+?)"').findall(link)[0]
                    frame = "http://www.meocanaltv.com/embed/"+tempId+".php";
                    ref_data = {'Referer': linkescolha,'User-Agent':user_agent}
                    link= abrir_url_tommy(frame,ref_data)
                    if re.search('embed.js',link):
                        link+= abrir_url_tommy(re.compile('src="([^"]+?)embed.js"').findall(link)[0] + 'embed.js',ref_data).decode('string-escape')
                    descobrirresolver(frame, nome,link,zapping,nomeserver)

                else: descobrirresolver(linkescolha, nome,False,zapping,nomeserver)


            elif re.search('gosporttv',linkescolha):
                marcador="Pre-catcher: thesporttv.eu"; print marcador
                link= clean(abrir_url(linkescolha))
                try:
                    linkcod=re.compile("id='(.+?)'.+?</script><script type='text/javascript' src='"+SptveuURL +"/teste/").findall(link)[0]
                    descobrirresolver(SptveuURL+ '/teste/c0d3r.php?id=' + linkcod,nome,'hdm1.tv',zapping,nomeserver)
                except:
                    frame=re.compile('</p>[^<]*<iframe allowtransparency="true" frameborder="0" scrolling="[^"]+?" src="([^"]+?)"').findall(link)[0]
                    frame=frame.replace('sporttvhdmi.com','gosporttv.com')
                    link= clean(abrir_url(frame))
                    if re.search('var urls = new Array',link):
                        framedupla=re.compile('new Array.+?"(.+?)".+?"(.+?)"').findall(link)[0]
                        if framedupla[0]==framedupla[1]: frame=framedupla[0]
                        else:
                            if activado==True: opcao=True
                            else:opcao= xbmcgui.Dialog().yesno("TV Portuguesa", "Escolha um stream da lista dos disponiveis.", "", "","Stream Extra", 'Stream Principal')
                            if opcao: frame=framedupla[0]
                            else: frame=framedupla[1]

                    descobrirresolver(frame, nome,False,zapping,nomeserver)
            elif re.search('lvshd',linkescolha):
                marcador="Pre-catcher: livesoccerhd"; print marcador
                link= abrir_url(linkescolha)
                linkfinal= limparcomentarioshtml(link,linkescolha)
                endereco=re.compile('<iframe.+?src="(.+?)".+?</iframe></div>').findall(link)[0]
                descobrirresolver(endereco, nome,False,zapping,nomeserver)

            elif re.search('redweb',linkescolha):
                marcador="Pre-catcher: redweb"; print marcador
                c=re.compile('c=(.+?)&').findall(linkescolha)[0]
                s=re.compile('s=(.+?)&').findall(linkescolha)[0]
                i=re.compile('i=(.+?)&').findall(linkescolha)[0]
                form_data = {'c':c,'s':s,'i':i}
                ref_data = {'User-Agent':user_agent}
                html= abrir_url_tommy(RedwebURL + '/monitor.php',ref_data,form_data=form_data)
                descobrirresolver(linkescolha, nome,html,zapping,nomeserver)

            elif re.search('tvtuga',linkescolha):
                marcador="Pre-catcher: tvtuga"; print marcador
                ref_data = {'Referer': TVTugaURL,'User-Agent':user_agent}
                link= abrir_url_tommy(linkescolha,ref_data)
                p = re.compile('<meta.*?>')
                link=p.sub('', link)
                descobrirresolver(linkescolha, nome,link,zapping,nomeserver)

            else: descobrirresolver(linkescolha, nome,False,zapping,nomeserver)

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

