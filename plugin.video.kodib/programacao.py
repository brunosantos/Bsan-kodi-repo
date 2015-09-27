import datetime
import re
from default import name
from requests import abrir_url
from resources.lib.daring import selfAddon
from utils import horaportuguesa, clean


def p_todos():
    if selfAddon.getSetting("prog-lista3") == "false": return ''
    else:
        try:
            dia= horaportuguesa(True)

            listacanais='RTP1,RTP2,SIC,TVI,SPTV1,SPTV2,SPTV3,SPTV4,SPTV5,SLB,SLB2,PORTO,CMTV,RTPIN,SICK,SICM,SICN,SICR,TVI24,TVIFIC,HOLLW,AXN,AXNBL,AXNWH,FOX,FOXCR,FLIFE,FOXM,SYFY,DISNY,PANDA,MOTOR,DISCV,ODISS,HIST,NGC,EURSP,FASH,VH1,MTV,ABOLA,RTPAC,RTPA,RTPM,RTPMD,BIGGS,ETVHD,DISNYJ,CHELS,CAÇAP,TOROTV,DISCT,GLOBO,TVREC,EURS2,SCP,TPA,EURN,ARTV,TRACE'
            url='http://services.sapo.pt/EPG/GetChannelListByDateInterval?channelSiglas='+listacanais+'&startDate=' + dia +':01&endDate='+ dia + ':02'
            link= clean(abrir_url(url,erro=False))

            listas=re.compile('<Sigla>(.+?)</Sigla>.+?<Title>(.+?)</Title>.+?<Description>(.+?)</Description>').findall(link)
            canais={}
            for nomecanal, nomeprog, descricao in listas:
                canais[nomecanal]={'nomeprog':'(' + nomeprog + ')','descprog':descricao}
            return canais
        except: pass


def p_umcanal(listas,desejado,desc):
    try: return listas[desejado][desc]
    except: return ''


def programacao_canal():
    titles=[]
    sigla=name.replace('[','-')
    sigla=re.compile('B](.+?)/B]').findall(sigla)[0]
    siglacanal=sigla.replace('SPORTTV 1-','SPTV1').replace('SPORTTV 2-','SPTV2').replace('SPORTTV 3-','SPTV3').replace('SPORTTV 4-','SPTV4').replace('SPORTTV 5-','SPTV5').replace('SPORTTV LIVE-','SPTVL').replace('Discovery Channel-','DISCV').replace('AXN Black-','AXNBL').replace('AXN White-','AXNWH').replace('FOX Crime-','FOXCR').replace('FOX Life-','FLIFE').replace('FOX Movies-','FOXM').replace('Eurosport-','EURSP').replace('Hollywood-','HOLLW').replace('Canal Panda-','PANDA').replace('Benfica TV 1-','SLB').replace('Benfica TV 2-','SLB2').replace('Porto Canal-','PORTO').replace('SIC K-','SICK').replace('SIC Mulher-','SICM').replace('SIC Noticias-','SICN').replace('SIC Radical-','SICR').replace('TVI24-','TVI24').replace('TVI Ficção-','TVIFIC').replace('Mais TVI-','SEM').replace('Syfy-','SYFY').replace('Odisseia-','ODISS').replace('História-','HIST').replace('National Geographic Channel-','NGC').replace('MTV-','MTV').replace('CM TV-','CMTV').replace('RTP Informação-','RTPIN').replace('Disney Channel-','DISNY').replace('Motors TV-','MOTOR').replace('ESPN America-','SEM').replace('Fashion TV-','FASH').replace('MOV-','SEM').replace('A Bola TV-','ABOLA').replace('Panda Biggs-','BIGGS').replace('RTP 1-','RTP1').replace('RTP 2-','RTP2').replace('RTP Açores-','RTPAC').replace('RTP Madeira-','RTPMD').replace('RTP Memória-','RTPM').replace('Disney Junior-','DISNYJ').replace('RTP Africa-','RTPA').replace('Económico TV-','ETVHD').replace('Chelsea TV-','CHELS').replace('TV Globo-','GLOBO').replace('TV Record-','TVREC').replace('Eurosport 2-','EURS2').replace('Discovery Turbo-','DISCT').replace('Toros TV-','TOROTV').replace('Caça e Pesca-','CAÇAP').replace('Sporting TV-','SCP').replace('TPA Internacional-','TPA')
    siglacanal=siglacanal.replace('-','')
    dia= horaportuguesa(True)
    diaseguinte= horaportuguesa('diaseguinte')
    url='http://services.sapo.pt/EPG/GetChannelListByDateIntervalJson?channelSiglas='+siglacanal+'&startDate=' + dia +':01&endDate='+ diaseguinte + ':02'
    ref=int(0)
    link=abrir_url(url)
    titles.append('No ar: %s\n\n[B][COLOR white]Programação:[/COLOR][/B]' % name)

    programas=re.compile('{"Actor":.+?"Description":"(.+?)".+?"StartTime":".+?-.+?-(.+?) (.+?):(.+?):.+?".+?"Title":"(.+?)"').findall(link)
    for descprog,dia, horas,minutos, nomeprog in programas:
        ref=ref+1
        if dia==datetime.datetime.now().strftime('%d'): dia='Hoje'
        else: dia='Amanhã'
        titles.append('\n[B][COLOR blue]%s %s:%s[/COLOR][/B] - [B][COLOR gold]%s[/COLOR][/B] - %s' % (dia,horas,minutos,nomeprog,descprog))
    programacao='\n'.join(titles)

    try:
        xbmc.executebuiltin("ActivateWindow(10147)")
        window = xbmcgui.Window(10147)
        xbmc.sleep(100)
        window.getControl(1).setLabel('TV Portuguesa')
        window.getControl(5).setText(programacao)
    except: pass