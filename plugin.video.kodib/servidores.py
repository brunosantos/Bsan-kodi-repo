import re
import sys
from default import TVGenteURL, savefile, activado, openfile, cachepath, MEOURL, \
    RTPURL, TVCoresURL, TugastreamURL, TVGOURL, TVTugaURL, TVDezURL, mensagemok, mensagemprogresso, activadoextra, \
    debug, art
from preResolver import pre_resolvers
from requests import abrir_url_cookie
from utils import clean, savefile, openfile, horaportuguesa
from resources.lib.daring import selfAddon, tvporpath


def info_servidores():
    #tvgentelink= clean(abrir_url_cookie(CanalHDURL,erro=False))
    #print tvgentelink
    #tvgentefinal='\n'.join(re.compile('<h2(.+?)><img src="').findall(tvgentelink))
    #savefile('canalhd', tvgentefinal)
    if selfAddon.getSetting("fontes-tvgente") == "true":
        try:
            tvgentelink= clean(abrir_url_cookie(TVGenteURL + '/front.php',erro=False))
            tvgentefinal='\n'.join(re.compile('onclick="window.open(.+?)/></a>').findall(tvgentelink))
            savefile('tvgente', tvgentefinal)

            #savefile('tvgente', tvgentelink)
        except: savefile('tvgente', '')


def request_servidores(url,name,tamanho=0,gravador=False):
    #if name=='[B]Eventos[/B] (Cesarix/Rominhos)':
    #    obter_lista(name,url)
    #    return

    nomelista=name
    name=name.replace('[','-')
    nome=re.compile('B](.+?)/B]').findall(name)[0]
    nomega=nome.replace('-','')
    #GA("listacanais",nomega)
    titles=[]; ligacao=[]

    if url=='nada' and activado==True: todosact(nomelista)
    else:


        ### CASOS ESPECIAIS ###

        if re.search('Caça e Pesca',nomelista) or re.search('Toros TV',nomelista):
            titles.append('Pontucanal')
            ligacao.append('http://verlatelegratis.com')

        if re.search('Clubbing TV',nomelista):
            titles.append('Clubbing TV Oficial')
            ligacao.append('http://www.clubbingtv.com/jwsubscribe/clubbing.php')

        if re.search('SIC',nomelista):
            titles.append('SIC Oficial')
            if re.search('Noticias',nomelista):ligacao.append('stream://http://213.13.26.7:1936/live/_definst_/sicnoticias/playlist.m3u8')
            else:ligacao.append('stream://http://213.13.26.7:1936/live/_definst_/sic/playlist.m3u8')

        if re.search('TVI',nomelista):
            titles.append('TVI Oficial')
            if re.search('24',nomelista):ligacao.append('http://www.tvi.iol.pt/direto/tvi24')
            else:ligacao.append('http://www.tvi.iol.pt/direto')

        if re.search('Casa dos Segredos',nomelista):
            titles.append('TVI Oficial')
            ligacao.append('http://www.tvi.iol.pt/secretstory/direto')

        if re.search('TV Globo',nomelista):
            titles.append('Look-TVs')
            ligacao.append('http://look-tvs.com/globo/')

        if re.search('TRACE Urban',nomelista):
            titles.append('Trace Oficial')
            ligacao.append('http://www.dailymotion.com/video/x1ahn4f_live-trace-urban_music')

        if re.search('Virgin Radio TV',nomelista):
            titles.append('Virgin Radio TV')
            ligacao.append('stream://http://wow01.105.net/live/virgin1/playlist.m3u8')

        if re.search('DJing TV',nomelista):
            titles.append('DJing TV')
            ligacao.append('stream://http://www.djing.com/tv/noaudio_PT.m3u8')

        if re.search('TPA Internacional',nomelista):
            titles.append('Muntumedia')
            ligacao.append('http://roku.muntumedia.s3.amazonaws.com/playlisttv/T_TPAI.xml')
            titles.append('TPAi Live')
            ligacao.append('http://www.tpai.tv/tpai_rtmp_dynamic_streaming.xml')

        #if re.search('Sporting TV',nomelista):
        #    titles.append('Altas Emoções')
        #    ligacao.append(AltasEmocoesURL)

        #if re.search('SPORTTV 1',nomelista) or re.search('SPORTTV 2',nomelista)or re.search('SPORTTV 3',nomelista) or re.search('SPORTTV 4',nomelista) or re.search('SPORTTV 5',nomelista):
            #titles.append('[B]Torrent-TV.RU (acestream)[/B]')
            #ligacao.append('http://api.torrent-tv.ru/t/BgF2xM3fd1KWxgEVO21eprkQPkZi55b0LosbJU8oeZVikr1wPAmjkV%2ByixKZYNGt')

        if re.search('ARTV',nomelista):
            titles.append('ARTV Oficial')
            ligacao.append('stream://rtsp://www.canal.parlamento.pt/Live')

        #if selfAddon.getSetting("fontes-canalhd") == "true":
        #    try:
        #        canalhdref=int(0)
        #        canalhdlink=openfile('canalhd',pastafinal=cachepath).replace('+','Mais')
        #        nomecanalhd=nome.replace('RTP 1-','RTP 1').replace('RTP 2-','RTP 2').replace('TVI-','TVI').replace('FOX-','FOX').replace('AXN-','AXN').replace('SIC-','SIC').replace('AXN Black-','AXN Black').replace('AXN White-','AXN White').replace('FOX Life-','FOX Life').replace('FOX Crime-','FOX Crime').replace('FOX Movies-','FOX Movies').replace('SPORTTV 1-','Sportv 1').replace('SPORTTV 2-','Sportv 2').replace('SPORTTV 3-','Sportv 3').replace('SPORTTV 4-','Sportv 4').replace('SPORTTV 5-','Sportv 5').replace('Canal Panda-','Canal Panda').replace('Hollywood-','Canal Hollywood').replace('Eurosport-','Eurosport').replace('MOV-','MOV').replace('VH1-','VH1').replace('Porto Canal-','portocanal').replace('SIC Noticias-','Sic Noticias').replace('SIC Radical-','SIC Radical').replace('SIC Mulher-','SIC Mulher').replace('SIC K-','sick').replace('Big Brother VIP-','bigbrothervip').replace('TVI Ficção-','TVI Ficção').replace('Syfy-','Syfy').replace('Benfica TV 1-','Benfica TV').replace('Benfica TV 2-','Benfica TV').replace('CM TV-','cmtv').replace('RTP Africa-','rtpafrica').replace('RTP Informação-','RTP Informação').replace('Fashion TV-','fashiontv').replace('ESPN-','ESPN').replace('RTP Africa-','rtpafrica').replace('RTP Madeira-','rtpmadeira').replace('RTP Internacional-','rtpinternacional').replace('Casa dos Segredos 5-','casadossegredos').replace('Económico TV-','economicotv').replace('Sporting TV-','Sporting TV').replace('Chelsea TV-','Chelsea TV').replace('TVI24-','TVI 24').replace('Mais TVI-','TVI Mais').replace('MTV-','MTV').replace('História-','Canal História').replace('Odisseia-','Odisseia').replace('Discovery Channel-','Discovery Channel').replace('National Geographic Channel-','National Geographic').replace('Disney Channel-','Disney Channel')
        #        canalhd=re.compile('>'+nomecanalhd +'</h2><a href="([^"]+?)"').findall(canalhdlink)
        #        if canalhd:
        #            for codigo in canalhd:
        #                canalhdref=int(canalhdref + 1)
        #                if len(canalhd)==1: canalhd2=str('')
        #                else: canalhd2=' #' + str(canalhdref)
        #                titles.append('CanalHD.tv' + canalhd2)
        #                ligacao.append(CanalHDURL + codigo)
        #    except: pass


        ########################################DESPORTOGRATIS############################
        if selfAddon.getSetting("fontes-desportogratis") == "true":
            try:
                desgrref=int(0)
                desgrlink=openfile('desgratis',pastafinal=cachepath)
                nomedesgr=nome.replace('SPORTTV 1-','1.html').replace('SPORTTV 2-','2.html').replace('SPORTTV 3-','3.html').replace('SPORTTV 4-','4.html').replace('SPORTTV 5-','4.html').replace('SPORTTV LIVE-','4.html').replace('Benfica TV 1-','5.html').replace('Benfica TV 2-','5.html')
                desgr=re.compile('<a href="http://www.desportogratis.com/'+nomedesgr+'" target="iframe"><form>').findall(desgrlink)
                if desgr:
                    for resto in desgr:
                        desgrref=int(desgrref + 1)
                        if len(desgr)==1:
                            desgr2=str('')
                        else:
                            desgr2=' #' + str(desgrref)
                        titles.append('Desporto Grátis' + desgr2)
                        ligacao.append('http://www.desportogratis.com/' + nomedesgr)

            except: pass

        if selfAddon.getSetting("fontes-meocanaltv") == "true":
            try:
                meocanaltv=False
                meocanaltvref=int(0)
                meocanaltvlink=openfile('meocanaltv',pastafinal=cachepath)
                nomemeocanaltv=nome.replace('RTP 1-','RTP 1').replace('RTP 2-','RTP 2').replace('RTP Informação-','RTP INFORMACAO').replace('RTP Africa-','RTP AFRICA').replace('RTP Madeira-','RTP MADEIRA').replace('RTP Internacional-','RTP INTERNACIONAL').replace('RTP Açores-','RTP ACORES').replace('RTP Memória-','RTP MEMORIA').replace('SIC-','SIC').replace('TVI-','TVI').replace('SPORTTV 1-','Sport TV em Direto').replace('Big Brother VIP-','BB VIP').replace('SIC K-','SIC KIDS').replace('SIC Radical-','SIC RADICAL').replace('SIC Mulher-','SIC MULHER').replace('SIC Noticias-','SIC NOTICIAS Online').replace('TVI24-','TVI 24').replace('Hollywood-','HOLLYWOOD').replace('MOV-','CANAL MOV').replace('AXN-','AXN').replace('AXN Black-','AXN BLACK').replace('AXN White-','AXN WHITE').replace('FOX-','FOX').replace('FOX Crime-','FOX CRIME').replace('FOX Life-','FOX LIFE').replace('FOX Movies-','FOX MOVIES').replace('Canal Panda-','CANAL PANDA').replace('Discovery Channel-','DISCOVERY CHANNEL').replace('Eurosport-','EUROSPORT 1').replace('Benfica TV 1-','Benfica TV online').replace('Benfica TV 2-','Benfica TV online').replace('Porto Canal-','PORTO CANAL').replace('Syfy-','SYFY').replace('Odisseia-','CANAL ODISSEIA').replace('História-','CANAL HISTÓRIA').replace('National Geographic Channel-','NATIONAL GEOGRAPHIC').replace('MTV-','MTV').replace('Disney Channel-','DISNEY CHANNEL').replace('Panda Biggs-','PANDA BIGGS').replace('Motors TV-','MOTORS TV').replace('ESPN-','ESPN Online BR').replace('ESPN America-','ESPN Online BR').replace('A Bola TV-','A BOLA TV').replace('Casa dos Segredos 5-','Secret Story 4 em Direto').replace('CM TV-','CM TV').replace('TVI Ficção-','TVI FICCAO').replace('Panda Biggs-','Panda Biggs').replace('Económico TV-','Económico TV - Emissão Online').replace('Disney Junior-','Canal Disney Junior').replace('TV Record-','Record Online ao Vivo').replace('Discovery Turbo-','Discovery Turbo Brasil').replace('Caça e Pesca-','Caza y Pesca').replace('Mais TVI-','+TVI').replace('Eurosport 2-','EUROSPORT 2')
                meocanaltv=re.compile('"(.+?)">%s<' % (nomemeocanaltv)).findall(meocanaltvlink)
                if meocanaltv:
                    for codigo in meocanaltv:
                        meocanaltvref=int(meocanaltvref + 1)
                        if len(meocanaltv)==1: meocanaltv2=str('')
                        else: meocanaltv2=' #' + str(meocanaltvref)
                        titles.append('MEOCanal TV' + meocanaltv2)
                        ligacao.append(MEOURL + codigo)
            except: pass

        ########################################RTPPLAY############################
        if selfAddon.getSetting("fontes-rtpplay") == "true":
            try:
                rtpplay=False
                rtpplayref=int(0)
                rtpplaylink=openfile('rtpplay',pastafinal=cachepath)
                nomertpplay=nome.replace('RTP 1-','rtp1').replace('RTP 2-','rtp2').replace('RTP Informação-','rtpinformacao').replace('RTP Africa-','rtpafrica').replace('RTP Madeira-','rtpmadeira').replace('RTP Internacional-','rtpinternacional').replace('RTP Açores-','rtpacores').replace('RTP Memória-','rtpmemoria')
                rtpplay=re.compile('id="' + nomertpplay + '" title=".+?" href="(.+?)">').findall(rtpplaylink)
                if rtpplay:
                    for codigo in rtpplay:
                        rtpplayref=int(rtpplayref + 1)
                        if len(rtpplay)==1: rtpplay2=str('')
                        else: rtpplay2=' #' + str(rtpplayref)
                        titles.append('RTP Play' + rtpplay2)
                        ligacao.append(RTPURL + codigo)
            except: pass

        ########################################TV A CORES############################
        if selfAddon.getSetting("fontes-tvacores") == "true":
            try:
                tvacoresref=int(0)
                tvacoreslink=openfile('tvacores',pastafinal=cachepath)
                nometvacores=nome.replace('RTP 1-','RTP 1 Online').replace('RTP 2-','RTP 2 Online').replace('SIC-','SIC Online').replace('TVI-','TVI Online').replace('SPORTTV 1-','Sport TV em Direto').replace('Big Brother VIP-','BB VIP').replace('SIC K-','SIC K Online').replace('SIC Radical-','SIC Radical Online').replace('SIC Mulher-','SIC Mulher Online').replace('SIC Noticias-','SIC Noticias Online').replace('TVI24-','TVI24 online').replace('Hollywood-','Canal Hollywood').replace('MOV-','Canal MOV').replace('AXN-','AXN Portugal').replace('AXN Black-','AXN Black Online').replace('AXN White-','AXN White online').replace('FOX-','Fox Online PT').replace('FOX Crime-','FOX Crime Online').replace('FOX Life-','FOX Life Online').replace('FOX Movies-','FOX Movies Portugal').replace('Canal Panda-','Canal Panda').replace('Discovery Channel-','Discovery Channel PT').replace('Eurosport-','Eurosport Portugal').replace('Benfica TV 1-','Benfica TV online').replace('Benfica TV 2-','Benfica TV online').replace('Porto Canal-','Porto Canal - Emissão Online').replace('Syfy-','SYFY Channel Portugal').replace('Odisseia-','Canal Odisseia').replace('História-','Canal Historia Portugal').replace('National Geographic Channel-','National Geographic PT').replace('MTV-','MTV Portugal').replace('RTP Açores-','RTP Açores Online').replace('RTP Africa-','RTP África Online').replace('RTP Informação-','RTP Informação - Emissão Online').replace('RTP Madeira-','RTP Madeira Online').replace('RTP Memória-','RTP Memória').replace('Disney Channel-','Disney Portugal').replace('Panda Biggs-','Panda Biggs').replace('Motors TV-','Motors TV Online').replace('ESPN-','ESPN Online BR').replace('ESPN America-','ESPN Online BR').replace('A Bola TV-','A Bola TV').replace('RTP Africa-','RTP Africa').replace('RTP Madeira-','RTP Madeira').replace('RTP Internacional-','RTP Internacional').replace('RTP Açores-','RTP Açores').replace('A Bola TV-','A Bola TV').replace('Casa dos Segredos 5-','A Casa dos Segredos').replace('CM TV-','CMTV em direto').replace('TVI Ficção-','TVI Ficção online').replace('Panda Biggs-','Panda Biggs').replace('Económico TV-','Económico TV - Emissão Online').replace('Disney Junior-','Canal Disney Junior').replace('TV Record-','Record Online ao Vivo').replace('Discovery Turbo-','Discovery Turbo Brasil').replace('Caça e Pesca-','Caza y Pesca').replace('Sporting TV-','Sporting TV online')
                tvacores=re.compile('<a href="(.*?)">'+nometvacores+'</a>').findall(tvacoreslink)
                if tvacores:
                    for codigo in tvacores:
                        tvacoresref=int(tvacoresref + 1)
                        if len(tvacores)==1: tvacores2=str('')
                        else: tvacores2=' #' + str(tvacoresref)
                        titles.append('TV a Cores' + tvacores2)
                        urlembed=TVCoresURL.replace('http://mytvfree.mehttp://antena.mytvfree.me','http://antena.mytvfree.me/')
                        ligacao.append(TVCoresURL + codigo)
                        #ligacao.append('http://mytvfree.mehttp://antena.mytvfree.me/sic.php')
                        #ligacao.append('http://antena24.com/sic.php')
            except: pass

        ########################################TUGASTREAM############################
        if selfAddon.getSetting("fontes-tugastream") == "true":
            try:
                tugastreamref=int(0)
                tugastreamlink=openfile('tugastream',pastafinal=cachepath)
                nometugastream=nome.replace('RTP 1-','rtp1').replace('RTP 2-','rtp2').replace('TVI-','tvi').replace('FOX-','fox').replace('AXN-','axn').replace('SIC-','sic').replace('AXN Black-','axnblack').replace('AXN White-','axnwhite').replace('FOX Life-','foxlife').replace('FOX Crime-','foxcrime').replace('FOX Movies-','foxmovies').replace('SPORTTV 1-','sporttv1').replace('SPORTTV 2-','sporttv2').replace('SPORTTV 3-','sporttv3').replace('SPORTTV 4-','sporttv4').replace('SPORTTV 5-','sporttv5').replace('Canal Panda-','panda').replace('Hollywood-','hollywood').replace('Eurosport-','eurosport').replace('MOV-','mov').replace('VH1-','vh1').replace('Porto Canal-','portocanal').replace('SIC Noticias-','sicnoticias').replace('SIC Radical-','sicradical').replace('SIC Mulher-','sicmulher').replace('SIC K-','sick').replace('Big Brother VIP-','bigbrothervip').replace('TVI Ficção-','tvificcao').replace('Syfy-','syfy').replace('Benfica TV 1-','benficatv').replace('Benfica TV 2-','benficatv').replace('CM TV-','cmtv').replace('RTP Africa-','rtpafrica').replace('RTP Informação-','rtpinformacao').replace('Fashion TV-','fashiontv').replace('ESPN-','espn').replace('RTP Africa-','rtpafrica').replace('RTP Madeira-','rtpmadeira').replace('RTP Internacional-','rtpinternacional').replace('Casa dos Segredos 5-','casadossegredos').replace('Económico TV-','economicotv')
                tugastream=re.compile('<a href="'+nometugastream + '(.+?)php">').findall(tugastreamlink)
                if tugastream:
                    for codigo in tugastream:
                        tugastreamref=int(tugastreamref + 1)
                        if len(tugastream)==1: tugastream2=str('')
                        else: tugastream2=' #' + str(tugastreamref)
                        titles.append('Tugastream' + tugastream2)
                        ligacao.append(TugastreamURL + nometugastream + codigo + 'php?altura=432&largura=768')
            except: pass

        ########################################TVGENTE############################
        if selfAddon.getSetting("fontes-tvgente") == "true":
            try:
                tvgenteref=int(0)
                tvgentelink = openfile('tvgente')
                nometvgente=nome.replace('SPORTTV 1-','sptv1novo.png').replace('SPORTTV 2-','sptv2novo.png').replace('SPORTTV 3-','sptv3novo.png').replace('SPORTTV 4-','jogooo.png').replace('SPORTTV 5-','sptv511.png').replace('Eurosport-','eurosportnovo.png').replace('Eurosport 2-','eurosport2novo.png').replace('ESPN-','espnnovo.png').replace('RTP 1-','1rtp.png').replace('RTP 2-','rtp2novo.png').replace('RTP Informação-','rtpinfonovo.png').replace('RTP Internacional-','rtp intnovo.png').replace('RTP Memória-','memoriartpnovo.png').replace('RTP Açores-','acoresnovortp.png').replace('RTP Madeira-','madeirartpnovo.png').replace('SIC-','3.gif').replace('SIC Noticias-','sicnnovo.png').replace('TVI-','tvinovo.png').replace('TVI24-','tvi24novo.png').replace('Porto Canal-','portonovo.png').replace('Benfica TV 1-','btvnovo.png').replace('Benfica TV 2-','btvnovo.png').replace('Sporting TV-','sportingtv.png').replace('A Bola TV-','biolatv.png').replace('CM TV-','cmtv.png').replace('Económico TV-','ecnovo.png').replace('FOX-','foxnovo.png').replace('Discovery Channel-','discnovo.png').replace('História-','historia').replace('Casa dos Segredos 5-','casa do putedo1.jpg')
                tvgente=re.compile("\('(.+?)'.+?<img.+?" +nometvgente + '"').findall(tvgentelink)
                nometvgente=nome.replace('SPORTTV 1-','miga1.png').replace('SPORTTV 2-','miga2.png').replace('SPORTTV 3-','miga3.png').replace('SPORTTV 4-','miga 4.png').replace('SPORTTV 5-','miga5.png').replace('Benfica TV 1-','btv11.png').replace('Benfica TV 2-','btv11.png').replace('SIC Noticias-','hd1sic.png').replace('Sporting TV-','testesporting.png')
                tvgente+=re.compile("\('(.+?)'.+?<img.+?" +nometvgente + '"').findall(tvgentelink)

                #new way to get stuff without the need to change source.
                #nometvgente=nome.replace('RTP 1-','RTP 1 Online').replace('RTP 2-','RTP 2 Online').replace('SIC-','SIC Online').replace('TVI-','TVI Online').replace('SPORTTV 1-','Sport TV em Direto').replace('Big Brother VIP-','BB VIP').replace('SIC K-','SIC K Online').replace('SIC Radical-','SIC Radical Online').replace('SIC Mulher-','SIC Mulher Online').replace('SIC Noticias-','SIC Noticias Online').replace('TVI24-','TVI24 online').replace('Hollywood-','Canal Hollywood').replace('MOV-','Canal MOV').replace('AXN-','AXN Portugal').replace('AXN Black-','AXN Black Online').replace('AXN White-','AXN White online').replace('FOX-','Fox Online PT').replace('FOX Crime-','FOX Crime Online').replace('FOX Life-','FOX Life Online').replace('FOX Movies-','FOX Movies Portugal').replace('Canal Panda-','Canal Panda').replace('Discovery Channel-','Discovery Channel PT').replace('Eurosport-','Eurosport Portugal').replace('Benfica TV 1-','Benfica TV online').replace('Benfica TV 2-','Benfica TV online').replace('Porto Canal-','Porto Canal - Emissão Online').replace('Syfy-','SYFY Channel Portugal').replace('Odisseia-','Canal Odisseia').replace('História-','Canal Historia Portugal').replace('National Geographic Channel-','National Geographic PT').replace('MTV-','MTV Portugal').replace('RTP Açores-','RTP Açores Online').replace('RTP Africa-','RTP África Online').replace('RTP Informação-','RTP Informação - Emissão Online').replace('RTP Madeira-','RTP Madeira Online').replace('RTP Memória-','RTP Memória').replace('Disney Channel-','Disney Portugal').replace('Panda Biggs-','Panda Biggs').replace('Motors TV-','Motors TV Online').replace('ESPN-','ESPN Online BR').replace('ESPN America-','ESPN Online BR').replace('A Bola TV-','A Bola TV').replace('RTP Africa-','RTP Africa').replace('RTP Madeira-','RTP Madeira').replace('RTP Internacional-','RTP Internacional').replace('RTP Açores-','RTP Açores').replace('A Bola TV-','A Bola TV').replace('Casa dos Segredos 5-','A Casa dos Segredos').replace('CM TV-','CMTV em direto').replace('TVI Ficção-','TVI Ficção online').replace('Panda Biggs-','Panda Biggs').replace('Económico TV-','Económico TV - Emissão Online').replace('Disney Junior-','Canal Disney Junior').replace('TV Record-','Record Online ao Vivo').replace('Discovery Turbo-','Discovery Turbo Brasil').replace('Caça e Pesca-','Caza y Pesca').replace('Sporting TV-','Sporting TV online')
                #tvgente=re.compile('<a href="(.*?)'+nometvgente+'..htm"').findall(tvgentelink)
                if tvgente:
                    for codigo in tvgente:
                        tvgenteref=int(tvgenteref + 1)
                        if len(tvgente)==1: tvgente2=str('')
                        else: tvgente2=' ' + str(tvgenteref)
                        titles.append('TV Gente' + tvgente2)
                        ligacao.append(codigo)
            except: pass

        if re.search('SPORTTV 1 HD',nomelista) or re.search('SPORTTV 1',nomelista):
            titles.append('TVGO.be')
            ligacao.append(TVGOURL)

        if re.search('SPORTTV 2',nomelista):
            titles.append('TVGO.be')
            ligacao.append(TVGOURL + 'sport2.html')


        ########################################TVTUGA############################
        if selfAddon.getSetting("fontes-tvtuga") == "true":
            try:
                tvtugaref=int(0)
                tvtugalink=openfile('tvtuga',pastafinal=cachepath)

                nometvtuga=nome.replace('RTP 1-','rtp-1').replace('RTP 2-','rtp-2').replace('TVI-','tvi').replace('FOX-','fox').replace('AXN-','axn').replace('SIC-','sic').replace('AXN Black-','axnblack').replace('AXN White-','axn-white').replace('FOX Life-','fox-life').replace('FOX Crime-','fox-crime').replace('FOX Movies-','fox-movies').replace('SPORTTV 1-','sporttv1').replace('SPORTTV 2-','sporttv2').replace('SPORTTV 3-','sporttv3').replace('SPORTTV 4-','sporttvlive').replace('SPORTTV LIVE-','sporttvlive').replace('Canal Panda-','canal-panda').replace('Hollywood-','canal-hollywood').replace('Eurosport-','eurosport').replace('MOV-','mov').replace('VH1-','vh1').replace('Porto Canal-','portocanal').replace('SIC Noticias-','sic-noticias').replace('SIC Radical-','sicradical').replace('SIC Mulher-','sicmulher').replace('SIC K-','sick').replace('Big Brother VIP-','bigbrothervip').replace('TVI Ficção-','tvi-ficcao').replace('Syfy-','syfy').replace('Benfica TV 1-','benfica-tv').replace('Benfica TV 2-','benfica-tv').replace('CM TV-','cm-tv').replace('RTP Africa-','rtp-africa').replace('RTP Informação-','rtp-informacao').replace('Fashion TV-','fashiontv').replace('ESPN-','espn').replace('A Bola TV-','abola-tv').replace('Casa dos Segredos 4-','secret-story-4-casa-dos-segredos').replace('RTP Açores-','rtp-acores').replace('RTP Internacional-','rtp-internacional').replace('RTP Madeira-','rtp-madeira').replace('RTP Memória-','rtp-memoria').replace('TVI24-','tvi-24').replace('Panda Biggs-','panda-biggs').replace('Económico TV-','economico-tv').replace('Eurosport 2-','eurosport-2').replace('Casa dos Segredos 5-','secret-story-5').replace('Euronews-','euronews')

                tvtuga=re.compile('value="http://www.tvtuga.com/'+nometvtuga+'(.+?)">').findall(tvtugalink)
                if tvtuga:
                    for codigo in tvtuga:
                        tvtugaref=int(tvtugaref + 1)
                        if len(tvtuga)==1: tvtuga2=str('')
                        else: tvtuga2=' #' + str(tvtugaref)
                        titles.append('TVTuga' + tvtuga2)
                        ligacao.append(TVTugaURL + '/' + nometvtuga + codigo)
            except: pass


        ########################################TVDEZ############################
        if selfAddon.getSetting("fontes-tvdez") == "true":
            try:
                tvdezref=int(0)
                tvdezlink=openfile('tvdez',pastafinal=cachepath)
                tvdezlink=tvdezlink.replace('+ TVI','Mais TVI')
                nometvdez=nome.replace('RTP 1-','RTP').replace('RTP 2-','RTP 2').replace('FOX-','FOX').replace('AXN-','AXN').replace('AXN Black-','AXN Black').replace('AXN White-','AXN White').replace('FOX Life-','FOX Life').replace('FOX Crime-','FOX Crime').replace('FOX Movies-','FOX Movies').replace('SPORTTV 3-','Sport TV 3').replace('SPORTTV 4-','Sport TV 4').replace('SPORTTV 5-','Sport TV 5').replace('SPORTTV LIVE-','Sporttv Live').replace('Canal Panda-','Canal Panda').replace('Hollywood-','Hollywood').replace('Eurosport-','Eurosport').replace('MOV-','Canal MOV').replace('VH1-','VH1 Hits').replace('Porto Canal-','Porto Canal').replace('SIC Radical-','SIC Radical').replace('SIC Mulher-','SIC Mulher').replace('SIC K-','SIC K').replace('TVI Ficção-','TVI Fic&ccedil;&atilde;o').replace('Discovery Channel-','Discovery Channel').replace('TVI24-','TVI 24').replace('Mais TVI-','Mais TVI').replace('Syfy-','Syfy').replace('Odisseia-','Odisseia').replace('História-','Hist&oacute;ria').replace('National Geographic Channel-','National Geographic').replace('MTV-','MTV').replace('CM TV-','Correio da Manh&atilde; TV').replace('RTP Açores-','RTP A&ccedil;ores').replace('RTP Informação-','RTP Informa&ccedil;&atilde;o').replace('RTP Madeira-','RTP Madeira').replace('RTP Memória-','RTP Mem&oacute;ria').replace('Disney Channel-','Disney Channel').replace('Fashion TV-','Fashion TV').replace('Disney Junior-','Disney Junior').replace('Panda Biggs-','Panda Biggs').replace('Motors TV-','Motors TV').replace('ESPN-','ESPN Brasil').replace('ESPN America-','ESPN').replace('A Bola TV-','A Bola TV').replace('RTP Africa-','RTP Africa').replace('RTP Madeira-','RTP Madeira').replace('RTP Internacional-','RTP Internacional').replace('RTP Memória-','RTP Mem&oacute;ria').replace('RTP Açores-','RTP A&ccedil;ores').replace('Panda Biggs-','Panda Biggs').replace('Económico TV-','Econ&oacute;mico TV').replace('Chelsea TV-','Chelsea TV').replace('Disney Junior-','Disney Junior').replace('TV Globo-','TV Globo').replace('TV Record-','Rede Record').replace('Eurosport 2-','Eurosport 2').replace('Euronews-','EuroNews')
                tvdez=re.compile('<a href="(.+?)" title="'+nometvdez+'">').findall(tvdezlink)
                if not tvdez:
                    nometvdez=nome.replace('SPORTTV 1-','Sport TV 1').replace('SPORTTV 2-','Sport TV 2').replace('SIC-','SIC').replace('TVI-','TVI').replace('SIC Noticias-','SIC Not&iacute;cias').replace('Big Brother VIP-','Big Brother VIP 2013').replace('Benfica TV 1-','Benfica TV').replace('Benfica TV 2-','Benfica TV').replace('Casa dos Segredos 5-','Casa dos segredos 5 - TVI Direct')
                    tvdez=re.compile('<a href="(.+?)" title="'+nometvdez+'">').findall(tvdezlink)
                    nometvdez=nome.replace('SPORTTV 1-','Sporttv em Directo').replace('SPORTTV 2-','Sporttv 2').replace('SIC-','SIC Online - Stream 2').replace('TVI-','TVI Online - Stream 2').replace('SIC Noticias-','SIC Not&iacute;cias Online').replace('Big Brother VIP-','Big Brother Portugal').replace('Benfica TV 1-','Benfica-TV').replace('Benfica TV 2-','Benfica-TV').replace('Casa dos Segredos 5-','Secret Story 5')
                    tvdez+=re.compile('<a href="(.+?)" title="'+nometvdez+'">').findall(tvdezlink)
                    nometvdez=nome.replace('SPORTTV 1-','Sporttv HD')
                    tvdez+=re.compile('<a href="(.+?)" title="'+nometvdez+'">').findall(tvdezlink)
                if tvdez:
                    for codigo in tvdez:
                        tvdezref=int(tvdezref + 1)
                        if len(tvdez)==1: tvdez2=str('')
                        else: tvdez2=' #' + str(tvdezref)
                        titles.append('TVDez' + tvdez2)
                        ligacao.append(TVDezURL + codigo)
            except: pass


        if len(ligacao)==1: index=0
        elif activado==True: index=0
        elif len(ligacao)==0: ok=mensagemok('TV Portuguesa', 'Nenhum stream disponivel.'); return
        else: index = xbmcgui.Dialog().select('Escolha o servidor', titles)
        if index > -1:
            if activado==False:
                mensagemprogresso.create('TV Portuguesa', 'A carregar stream. (' + titles[index] + ')','Por favor aguarde...')
                mensagemprogresso.update(0)
                if mensagemprogresso.iscanceled(): mensagemprogresso.close()
                pre_resolvers(titles,ligacao,index,nome,zapping=gravador)
            else:
                index=-1

                for linkescolha in ligacao:
                    index=index+1
                    pre_resolvers(titles,ligacao,index,nome,tamanho=tamanho,zapping=gravador)

                activadoextra2=set(activadoextra)
                thumb=nome.replace('Mais TVI-','maistvi-ver2.png').replace('AXN-','axn-ver2.png').replace('FOX-','fox-ver2.png').replace('RTP 1-','rtp1-ver2.png').replace('RTP 2-','rtp2-ver2.png').replace('SIC-','sic-ver3.png').replace('SPORTTV 1-','sptv1-ver2.png').replace('SPORTTV 1 HD-','sptvhd-ver2.png').replace('SPORTTV 2-','sptv2-ver2.png').replace('SPORTTV 3-','sptv3-ver2.png').replace('SPORTTV 4-','sptv4-ver2.png').replace('SPORTTV LIVE-','sptvlive-ver1.png').replace('TVI-','tvi-ver2.png').replace('Discovery Channel-','disc-ver2.png').replace('AXN Black-','axnb-ver2.png').replace('AXN White-','axnw-ver2.png').replace('FOX Crime-','foxc-ver2.png').replace('FOX Life-','foxl-ver3.png').replace('FOX Movies-','foxm-ver2.png').replace('Eurosport-','eusp-ver2.png').replace('Hollywood-','hwd-ver2.png').replace('MOV-','mov-ver2.png').replace('Canal Panda-','panda-ver2.png').replace('VH1-','vh1-ver2.png').replace('Benfica TV 1-','btv1-ver1.png').replace('Benfica TV 2-','btv2-ver1.png').replace('Porto Canal-','pcanal-ver2.png').replace('Big Brother VIP-','bbvip-ver2.png').replace('SIC K-','sick-ver2.png').replace('SIC Mulher-','sicm-ver3.png').replace('SIC Noticias-','sicn-ver2.png').replace('SIC Radical-','sicrad-ver2.png').replace('TVI24-','tvi24-ver2.png').replace('TVI Ficção-','tvif-ver2.png').replace('Syfy-','syfy-ver1.png').replace('Odisseia-','odisseia-ver1.png').replace('História-','historia-ver1.png').replace('National Geographic Channel-','natgeo-ver1.png').replace('MTV-','mtv-ver1.png').replace('CM TV-','cmtv-ver1.png').replace('RTP Informação-','rtpi-ver1.png').replace('Disney Channel-','disney-ver1.png').replace('Motors TV-','motors-ver1.png').replace('ESPN America-','espna-ver1.png').replace('Fashion TV-','fash-ver1.png').replace('A Bola TV-','abola-ver1.png').replace('Casa dos Segredos 5-','casadseg-ver1.png').replace('RTP Açores-','rtpac-ver1.png').replace('RTP Internacional-','rtpint-ver1.png').replace('RTP Madeira-','rtpmad-ver1.png').replace('RTP Memória-','rtpmem-ver1.png').replace('RTP Africa-','rtpaf-ver1.png').replace('Panda Biggs-','pbiggs-ver1.png').replace('TV Record-','record-v1.png').replace('TV Globo-','globo-v1.png').replace('Eurosport 2-','eusp2-ver1.png').replace('Discovery Turbo-','discturbo-v1.png').replace('Toros TV-','toros-v1.png').replace('Chelsea TV-','chel-v1.png').replace('Disney Junior-','djun-ver1.png').replace('Económico TV-','econ-v1.png').replace('Caça e Pesca-','cacapesca-v1.png').replace('TPA Internacional-','tpa-ver1.png').replace('TRACE Urban-','traceu.png').replace('Virgin Radio TV-','virginr.png').replace('DJing TV-','djingtv.png')

                nome=nome.replace('-','')
                SIM='</link>\n<link>'.join(activadoextra2)
                if SIM=='':
                    return ''
                else:
                    SIM='<link>%s</link>' % (SIM)
                    if thumb=='tvif-ver2.png':nome='TVI Ficcao'
                    elif thumb=='historia-ver1.png': nome='Historia'
                    elif thumb=='rtpac-ver1.png': nome='RTP Acores'
                    elif thumb=='rtpi-ver1.png': nome='RTP Informacao'
                    elif thumb=='rtpmem-ver1.png': nome='RTP Memoria'
                    elif thumb=='econ-v1.png': nome='Economico TV'
                    elif thumb=='cacapesca-v1.png': nome='Caca e Pesca'
                    CONTEUDO='<item>\n<title>%s</title>\n%s\n<thumbnail>%s</thumbnail>\n</item>' % (nome,SIM,thumb)
                return CONTEUDO


def todosact(parametro):
    LOLI=['<item>\n<title>Actualizado: ' + horaportuguesa(True).replace('%20',' ') + '</title>\n<link>nada</link>\n<thumbnail>nada</thumbnail>\n</item>']
    dialog = xbmcgui.Dialog()
    mensagemprogresso.create('TV Portuguesa', 'A criar lista.','Por favor aguarde...')
    if re.search('Lista Completa',parametro):
        canaison= openfile(('canaison'))
        canaison=canaison.replace('[','')
        lista=re.compile('B](.+?)/B]').findall(canaison)
        tamanhototal=int(len(lista))
        tamanho=int(-1)
        for nomes in lista:
            tamanho=tamanho+1
            tamanhoenviado=(tamanho*100)/tamanhototal
            print "Lista completa: Canal " + nomes
            global activadoextra
            activadoextra=[]
            SIM= request_servidores('ignore','[B]' + nomes + '[/B]',tamanho=tamanhoenviado)
            LOLI.append(SIM)
            AGORA='\n\n'.join(LOLI)
    else:
        SIM= request_servidores('ignore',parametro)
        LOLI.append(SIM)
        AGORA='\n\n'.join(LOLI)

    mensagemprogresso.close()

    debugfinal='\n'.join(debug)
    savefile('problema',debugfinal)

    keyb = xbmc.Keyboard('', 'Nome do ficheiro da lista')
    keyb.doModal()
    if (keyb.isConfirmed()):
        nomelista = keyb.getText()
        if nomelista=='': nomelista='lista'
    else: nomelista='lista'
    pastafinal = dialog.browse(int(0), "Local para guardar xml/m3u", 'myprograms')
    if not pastafinal: sys.exit(0)
    savefile(nomelista + '.xml',AGORA,pastafinal=pastafinal)
    m3uprep=['#EXTM3U#EXTM3U']
    openedfile= clean(AGORA)
    ya=re.compile('<item>(.+?)</item>').findall(openedfile)
    for lol in ya:
        chname=re.compile('<title>(.+?)</title>').findall(lol)[0]
        allstreams=False
        if allstreams==True:
            streams=re.compile('<link>(.+?)</link>').findall(lol)
            for umporum in streams:
                m3uprep.append('\n#EXTINF:-1,%s\n%s' % (chname,umporum))
        else:
            streams=re.compile('<link>(.+?)</link>').findall(lol)[0]
            m3uprep.append('\n#EXTINF:-1,%s\n%s' % (chname,streams))
    m3uprep='\n'.join(m3uprep)
    savefile(nomelista + '.m3u',m3uprep,pastafinal=pastafinal)
    xbmc.executebuiltin("XBMC.Notification(TV Portuguesa, Lista xml/m3u gravada,'100000'," + tvporpath + art + "icon32-ver1.png)")