import re
from default import BeachcamURL, SurflineURL, SurftotalURL, art
from utils import addDir
from requests import abrir_url
from resources.lib.daring import tvporpath

def praias():
    beachcams=[]
    try:
        temp= abrir_url(BeachcamURL + 'pt/livecams/')
        beachcams=re.compile('<a href="/pt/livecams/(.+?)">(.+?)</a>').findall(temp)
    except: print "Nao foi possivel obter as BeachCams"
    try:
        temp= abrir_url(SurflineURL + '/surf-report/portugal_2946/map/')
        beachcams+=re.compile('\tbackground-image:url./surfdata/images/icon_hdcam_blue.gif.\n\t\t\t\t\n                ;background-repeat:no-repeat;background-position:bottom left"\n                href="(.+?)">(.+?)</a>').findall(temp)
    except: print "Nao foi possivel obter as Surfline"
    try:
        temp=re.compile('Report<b class="caret">(.+?)</li></ul></li>').findall(abrir_url(SurftotalURL))[0]
        beachcams+=re.compile('<a href="(.+?)" >(.+?)</a>').findall(temp)
    except: print "Nao foi possivel obter as Surftotal"
    beachcams.sort(key=lambda t: t[1])
    for end,nome in beachcams:
        nome=nome.replace('&#227;','ã').replace('&#231;','ç').replace('&#237;','í').replace('&#180;','á')
        if re.search('surf-report',end):
            end=SurflineURL + end
            nome= '[B]%s[/B] (Surfline)' % nome
        elif re.search('camaras-report',end):
            end=SurftotalURL + end
            nome= '[B]%s[/B] (Surftotal)' % nome
        else:
            end=BeachcamURL + 'pt/livecams/' + end
            nome= '[B]%s[/B] (Beachcam.pt)' % nome
        addDir(nome,end,27,tvporpath + art + 'versao-ver2.png',len(beachcams),'',False)

