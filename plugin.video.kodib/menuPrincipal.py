from default import addDir, art, versao, addLink
from utils import versao_disponivel, addDir, addLink
from resources.lib.daring import tvporpath


def menu_principal():
    if xbmc.getCondVisibility('system.platform.linux') or xbmc.getCondVisibility('system.platform.windows') or xbmc.getCondVisibility('system.platform.osx'):
        addDir('Ver Gravações','nada',12,tvporpath + art + 'gravador-ver1.png',1,'Aceda à lista das gravações já efectuadas',False)
    disponivel=versao_disponivel()
    if disponivel==versao: addLink('Última versao (' + versao+ ')','',tvporpath + art + 'versao-ver2.png')
    else: addDir('Instalada v' + versao + ' | Actualização v' + disponivel,'nada',15,tvporpath + art + 'versao-ver2.png',1,'',False)
    addDir("Definições do addon",'nada',22,tvporpath + art + 'defs-ver2.png',1,'',False)
    addDir("[COLOR red][B]LER AVISO[/B][/COLOR]",'nada',23,tvporpath + art + 'aviso-ver2.png',1,'',False)
    xbmc.executebuiltin("Container.SetViewMode(500)")