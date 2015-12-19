# import sys
# import urllib
# import urlparse
# import xbmcgui
# import xbmcplugin
import xbmc, xbmcaddon, xbmcgui, xbmcplugin, urllib, urllib2, os, re, sys
from resources.lib.common_addon import Addon
import urlparse

# base_url = sys.argv[0]
# addon_handle = int(sys.argv[1])
# args = urlparse.parse_qs(sys.argv[2][1:])
#
my_addon = xbmcaddon.Addon()
use_sonar = my_addon.getSetting('use_sonar') == 'true'
# my_addon.setSetting('use_sonar', 'false')

load_backup = my_addon.getSetting('load_backup') == 'true'
# my_addon.setSetting('load_backup', 'false')

username = 'trial'
password = my_addon.getSetting('m3u_pwd')

if use_sonar:
    from m3uSonar import GetPwd

    password = GetPwd()
    my_addon.setSetting('m3u_pwd', password)
source = 'http://tvdasogra.com:8880/get.php?username=' + username + '&password=' + password + '&type=m3u&output=mpegts'
backupSource = 'https://dl.dropboxusercontent.com/s/35q79t3m9cwuqdj/tvdasograv2.m3u'

#
# xbmcplugin.setContent(addon_handle, 'movies')

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

def appendPydevRemoteDebugger():
    try:
        sys.path.append(
            "D:\\Kodi\\eclipse-cpp-mars-R-win32-x86_64\\eclipse\\plugins\\org.python.pydev_4.3.0.201508182223\\pysrc")
        import pydevd
        # import pysrc.pydevd as pydevd # with the addon script.module.pydevd, only use `import pydevd`
        # stdoutToServer and stderrToServer redirect stdout and stderr to eclipse console
        pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
        # pydevd.settrace('localhost', port=5678, stdoutToServer=True, stderrToServer=True)
    except ImportError:
        sys.stderr.write("Error: " + "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")
        sys.exit(1)


# appendPydevRemoteDebugger()

addon_id = 'plugin.video.sparrowtv'
addon = Addon(addon_id, sys.argv)
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))


def Index():
    if load_backup:
        GetLinks(backupSource)
    else:
        GetLinks(source)

# def GetLinksFromPlx(url):
#     link = open_url(url)
#     link = link.replace('\n', '').replace('#', '##')
#     try:
#         fanart = re.compile('background=(.+?)logo').findall(link)[0]
#     except:
#         fanart = re.compile('background=(.+?)thumb').findall(link)[0]
#     match = re.compile('#.+?#', re.DOTALL).findall(link)
#     for item in match:
#         match = re.compile('type=playlistthumb=(.+?)name=(.+?)URL=(.+?)#').findall(item)
#         for thumb, name, url in match:
#             addDir(name, url, thumb, fanart)
#         match = re.compile('type=videoname=(.+?)thumb=(.+?)URL=(.+?)#').findall(item)
#         for name, thumb, url in match:
#             addLink(name, url, thumb, fanart)


def GetLinks(url):
    link = open_url(url)
    match = re.compile(ur'#EXTINF.*,.*\nhttps?.*.ts').findall(link)
    for item in match:
        print item
        match = re.compile(ur'#EXTINF.*,(.*)\n(https?.*.ts)').findall(item)
        for name, url in match:
            print name + '\n' + url
            addLink(name, url)

def Play(url, iconimage):
    ok = False
    listItem = xbmcgui.ListItem(foldername, iconImage=icon, thumbnailImage=icon)
    listItem.setInfo(type="Video", infoLabels={"Title": foldername})
    ok = xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=listItem)
    try:
        xbmc.Player().play(url, listItem, False)
        return ok
    except:
        pass


def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    return link


def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def addLink(name, url, iconimage='', fanart='', description=''):
    pluginUrl = build_url({'url': urllib.quote_plus(url), 'mode': 'play', 'foldername': urllib.quote_plus(name),
                           'description': description})
    ok = False
    listItem = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
    listItem.setInfo(type="Video", infoLabels={"Title": name, 'plot': description})
    ok = xbmcplugin.addDirectoryItem(handle=addon_handle, url=pluginUrl, listitem=listItem, isFolder=False)
    return ok

def addDir(name, url, iconimage, fanart, description=''):
    pluginUrl = build_url({'url': urllib.quote_plus(url), 'mode': 'browse', 'foldername': urllib.quote_plus(name),
                           'description': description})
    ok = False
    listItem = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    listItem.setInfo(type="Video", infoLabels={"Title": name, 'plot': description})
    listItem.setProperty('fanart_image', fanart)
    ok = xbmcplugin.addDirectoryItem(handle=addon_handle, url=pluginUrl, listitem=listItem, isFolder=True)
    return ok


pluginUrl = None
name = None
mode = None
site = None
iconimage = None

try:
    site = urllib.unquote_plus(args.get('site')[0])
except:
    pass
try:
    pluginUrl = urllib.unquote_plus(args.get("url")[0])
except:
    pass
try:
    foldername = urllib.unquote_plus(args.get("foldername")[0])
except:
    pass
try:
    mode = args.get('mode', None)[0]
except:
    pass
try:
    iconimage = urllib.unquote_plus(args.get("iconimage"))
except:
    pass

print "Site: " + str(site)
print "Mode: " + str(mode)
print "URL: " + str(pluginUrl)
print "Name: " + str(name)

if mode == None or pluginUrl == None or len(pluginUrl) < 1:
    Index()
elif mode == 'browse':
    GetLinks(pluginUrl)
elif mode == 'play':
    Play(pluginUrl, iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
