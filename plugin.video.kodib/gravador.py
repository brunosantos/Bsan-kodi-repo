import datetime
import os
import re
import sys
from default import downloadPath, art, mensagemprogresso, gravadorpath, savefile
from requests import abrir_url
from resources.lib.daring import selfAddon, tvporpath
from utils import limpar, horaportuguesa, normalize, clean, savefile


def menugravador():
    if downloadPath=='':
        xbmcgui.Dialog().ok('TV Portuguesa','Necessitas de introduzir a pasta onde vão ficar','as gravações. Escolhe uma pasta com algum espaço','livre disponível.')
        dialog = xbmcgui.Dialog()
        pastafinal = dialog.browse(int(3), "Escolha pasta para as gravações", 'files')
        selfAddon.setSetting('pastagravador',value=pastafinal)
        return
    xbmc.executebuiltin("ReplaceWindow(VideoFiles," + downloadPath + ")")


def iniciagravador(finalurl,siglacanal,name,directo):
    print "A iniciar gravador 1/2"
    if downloadPath=='':
        xbmcgui.Dialog().ok('TV Portuguesa','Necessitas de introduzir a pasta onde vão ficar','as gravações. Escolhe uma pasta com algum espaço','livre disponível.')
        dialog = xbmcgui.Dialog()
        pastafinal = dialog.browse(int(3), "Escolha pasta para as gravações", 'files')
        selfAddon.setSetting('pastagravador',value=pastafinal)
        return
    if directo==True:
        if re.search('rtmp://',finalurl) or re.search('rtmpe://',finalurl):
        #if re.search('rtmp://',finalurl):
            finalurl=finalurl.replace('playPath=','-y ').replace('swfVfy=1','').replace('conn=','-C ').replace('live=true','-v').replace('swfUrl=','-W ').replace('pageUrl=','-p ').replace(' token=','-T ').replace('app=','-a ').replace('  ',' ').replace('timeout=','-m ')
            verifica_so('-r ' + finalurl,name,siglacanal,directo)
        else: xbmc.executebuiltin("XBMC.Notification(TV Portuguesa, Stream não gravável. Escolha outro.,'100000'," + tvporpath + art + "icon32-ver1.png)")


def verifica_so(args,nomecanal,siglacanal,directo):
    print "A iniciar gravador 2/2"
    mensagemprogresso.create('TV Portuguesa','A carregar gravador...')
    #correrdump(args,nomecanal,'windows',siglacanal,directo)
    if selfAddon.getSetting('rtmpdumpalternativo')=='':
        if xbmc.getCondVisibility('system.platform.windows'): correrdump(args,nomecanal,'gravador-windows',siglacanal,directo)
        elif xbmc.getCondVisibility('system.platform.osx'): correrdump(args,nomecanal,'gravador-mac86atv1',siglacanal,directo)
        elif xbmc.getCondVisibility('system.platform.linux'):
            if os.uname()[4] == "armv6l":
                pasta=os.path.join(gravadorpath,'rpi')
                basescript='#!/bin/sh\nexport LD_LIBRARY_PATH="%s"\n' % (pasta)
                correrdump(args,nomecanal,'gravador-rpi',siglacanal,directo,script=basescript)
            elif os.uname()[4] == "x86_64":
                pasta=os.path.join(gravadorpath,'linux64')
                basescript='#!/bin/sh\nexport LD_LIBRARY_PATH="%s"\n' % (pasta)
                correrdump(args,nomecanal,'gravador-linux64',siglacanal,directo,script=basescript)
            else:
                pasta=os.path.join(gravadorpath,'linux86')
                basescript='#!/bin/sh\nexport LD_LIBRARY_PATH="%s"\n' % (pasta)
                correrdump(args,nomecanal,'gravador-linux86',siglacanal,directo,script=basescript)
    else: correrdump(args,nomecanal,'alternativo',siglacanal,directo)


def correrdump(args,nomecanal,pathso,siglacanal,directo,script=False):
    import subprocess
    info=infocanal(siglacanal)
    escolha=0 #### inicializador
    mensagemprogresso.close()
    if info!=False and directo!='listas': escolha=listadeprogramas(info) #### se ha programacao, mostra lista
    if escolha==0:
        if info!=False and directo!='listas': #### ha programacao
            fimprograma=calculafinalprograma(info)
            tituloprograma=' - '+ re.compile('<Title>(.+?)</Title>').findall(info)[0]
            #nomecanal = nomecanal + tituloprograma
            minutosrestantes=fimprograma / 60
            opcao= xbmcgui.Dialog().yesno("TV Portuguesa", 'Faltam ' + str(minutosrestantes) + ' minutos para o fim do programa', "Deseja gravar o resto do programa ou", "definir um tempo de gravação?",'Definir tempo', 'Gravar restante')
            if opcao==1:
                if selfAddon.getSetting("acrescentogravacao") == "0": segundos=fimprograma
                elif selfAddon.getSetting("acrescentogravacao") == "1": segundos=fimprograma+120
                elif selfAddon.getSetting("acrescentogravacao") == "2": segundos=fimprograma+300
                elif selfAddon.getSetting("acrescentogravacao") == "3": segundos=fimprograma+600
                else: segundos=fimprograma + 120
                minutos=segundos/60
            else:
                minutos = -1
                while minutos < 1: minutos = int(xbmcgui.Dialog().numeric(0,"Num de minutos de gravacao"))
                segundos=minutos*60
        else:
            minutos = -1
            while minutos < 1: minutos = int(xbmcgui.Dialog().numeric(0,"Num de minutos de gravacao"))
            segundos=minutos*60
        nomecanal = limpar(re.sub('[^-a-zA-Z0-9_.()\\\/ ]+', '',  nomecanal))
        horaactual= horaportuguesa(False)

        if pathso=='alternativo': caminhodump=selfAddon.getSetting("rtmpdumpalternativo")
        else: caminhodump=os.path.join(gravadorpath,pathso)

        if xbmc.getCondVisibility('system.platform.linux'):
            st = os.stat(caminhodump)
            os.chmod(caminhodump, st.st_mode | stat.S_IEXEC)

        args=args.split(' ')
        typeargs=[]
        for types in args:
            if len(types) != 2: typeargs.append('"' + types + '"')
            else: typeargs.append(types)
        args=' '.join(typeargs)

        argumentos=args + ' -o "' + downloadPath + horaactual + ' - ' + nomecanal + '.flv" -B ' + str(segundos)
        #argumentos=args + ' -o "' + downloadPath + horaactual + '.flv" -B ' + str(segundos)

        if script:
            conteudoscript=script + xbmc.translatePath(os.path.join(gravadorpath,pathso))+ ' $1 ' + argumentos
            savefile('script.sh', conteudoscript ,pastafinal=gravadorpath)
            caminhodump=xbmc.translatePath(os.path.join(gravadorpath,'script.sh'))
            st = os.stat(caminhodump)
            os.chmod(caminhodump, st.st_mode | stat.S_IEXEC)
        try:
            #proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if script:
                proc = subprocess.Popen(caminhodump, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                #proc = subprocess.Popen(argumentos, executable=caminhodump + '.exe', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                cmd = '"%s" %s' % (caminhodump, argumentos)
                proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print "RTMPDump comecou a funcionar"
            xbmc.executebuiltin("XBMC.Notification(TV Portuguesa, Gravação de "+str(minutos)+" minutos iniciou,'10000'," + tvporpath + "/resources/art/icon32-ver1.png)")
            (stdout, stderr) = proc.communicate()
            print "RTMPDump parou de funcionar"
            stderr = normalize(stderr)
            if u'Download complete' in stderr:
                print 'stdout: ' + str(stdout)
                print 'stderr: ' + str(stderr)
                print "Download Completo!"
                xbmc.executebuiltin("XBMC.Notification(TV Portuguesa, Gravação efectuada com sucesso,'10000'," + tvporpath + "/resources/art/icon32-ver1.png)")
            else:
                print 'stdout: ' + str(stdout)
                print 'stderr: ' + str(stderr)
                print "Download Falhou!"
                xbmc.executebuiltin("XBMC.Notification(TV Portuguesa, Gravação falhou,'10000'," + tvporpath + "/resources/art/icon32-ver1.png)")
        except Exception:
            print ("Nao conseguiu abrir o programa")
            xbmc.executebuiltin("XBMC.Notification(TV Portuguesa, Erro ao abrir programa de gravação,'10000'," + tvporpath + "/resources/art/icon32-ver1.png)")
            (etype, value, traceback) = sys.exc_info()
            print "Erro etype: " + str(etype)
            print "Erro valor: " + str(value)
            print "Erro traceback: " + str(traceback)


def infocanal(siglacanal):
    if siglacanal=='SEM':
        print "Canal sem programacao."
        return False
    try:
        dia= horaportuguesa(True)
        diaseguinte= horaportuguesa('diaseguinte')
        url='http://services.sapo.pt/EPG/GetChannelListByDateInterval?channelSiglas='+siglacanal+'&startDate=' + dia +':01&endDate='+ diaseguinte + ':02'
        link= clean(abrir_url(url))
        return link
    except:
        print "Nao conseguiu capturar programacao."
        return False


def listadeprogramas(link):
    titles=[]
    ligacao=[]
    ref=int(0)
    programas=re.compile('<Title>(.+?)</Title>.+?<StartTime>.+?-.+?-(.+?) (.+?):(.+?):.+?</StartTime>').findall(link)
    for nomeprog,dia, horas,minutos in programas:
        ref=ref+1
        if dia==datetime.datetime.now().strftime('%d'): dia='Hoje'
        else: dia='Amanhã'
        if ref==2:
            titles.append('')
            titles.append('[COLOR red]A seguir: (não dá para gravar)[/COLOR]')
        if ref!=1:  titles.append(dia + ' ' + horas + ':' + minutos + ' - ' +nomeprog)
        else: titles.append(dia + ' ' + horas + ':' + minutos + ' - ' +nomeprog)
        ligacao.append('')
    index = xbmcgui.Dialog().select('Escolha o programa a gravar', titles)
    return index


def calculafinalprograma(link):
    fim=re.compile('<EndTime>(.+?)-(.+?)-(.+?) (.+?):(.+?):.+?</EndTime>').findall(link)[0]
    agora= horaportuguesa(False)
    inicio=re.compile('(.+?)-(.+?)-(.+?) (.+?)-(.+?)-').findall(agora)[0]
    start = datetime.datetime(year=int(inicio[0]), month=int(inicio[1]), day=int(inicio[2]), hour=int(inicio[3]), minute=int(inicio[4]))
    end = datetime.datetime(year=int(fim[0]), month=int(fim[1]), day=int(fim[2]), hour=int(fim[3]), minute=int(fim[4]))
    diff = end - start
    segundos= (diff.microseconds + (diff.seconds + diff.days * 24 * 3600) * 10**6) / 10**6
    return segundos