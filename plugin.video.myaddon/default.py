# import sys
# import urllib
# import urlparse
# import xbmcgui
# import xbmcplugin
# import xbmcaddon

# base_url = sys.argv[0]
# addon_handle = int(sys.argv[1])
# args = urlparse.parse_qs(sys.argv[2][1:])
#
# my_addon = xbmcaddon.Addon()
# my_setting = my_addon.getSetting('my_setting') # returns the string 'true' or 'false'
# my_addon.setSetting('my_setting', 'false')
#
# xbmcplugin.setContent(addon_handle, 'movies')
#
# def build_url(query):
#     return base_url + '?' + urllib.urlencode(query)
#
# mode = args.get('mode', None)
#
# if mode is None:
#     url = build_url({'mode': 'folder', 'foldername': 'Folder One'})
#     li = xbmcgui.ListItem('Folder One', iconImage='DefaultFolder.png')
#     xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
#
#     url = build_url({'mode': 'folder', 'foldername': 'Folder Two'})
#     li = xbmcgui.ListItem('Folder Two', iconImage='DefaultFolder.png')
#     #li.setProperty('fanart_image', my_addon.getAddonInfo('fanart'))
#     xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
#
#     xbmcplugin.endOfDirectory(addon_handle)
#
# elif mode[0] == 'folder':
#     foldername = args['foldername'][0]
#     url = 'http://localhost/some_video.mkv'
#     li = xbmcgui.ListItem(foldername + ' Video', iconImage='DefaultVideo.png')
#     li.setProperty('fanart_image', 'fanartb.jpg')
#     xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
#     xbmcplugin.endOfDirectory(addon_handle)

import xbmc, xbmcaddon, xbmcgui, xbmcplugin, urllib, urllib2, os, re, sys
from resources.lib.common_addon import Addon


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


appendPydevRemoteDebugger()

addon_id = 'plugin.video.direto'
addon = Addon(addon_id, sys.argv)
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))


def Index():
    GetLinks('https://dl.dropboxusercontent.com/s/35q79t3m9cwuqdj/tvdasograv2.m3u')


def GetLinksFromPlx(url):
    link = open_url(url)
    link = link.replace('\n', '').replace('#', '##')
    try:
        fanart = re.compile('background=(.+?)logo').findall(link)[0]
    except:
        fanart = re.compile('background=(.+?)thumb').findall(link)[0]
    match = re.compile('#.+?#', re.DOTALL).findall(link)
    for item in match:
        match = re.compile('type=playlistthumb=(.+?)name=(.+?)URL=(.+?)#').findall(item)
        for thumb, name, url in match:
            addDir(name, url, thumb, fanart)
        match = re.compile('type=videoname=(.+?)thumb=(.+?)URL=(.+?)#').findall(item)
        for name, thumb, url in match:
            addLink(name, url, thumb, fanart)


def GetLinks(url):
    link = open_url(url)
    # link = link.replace('\n', '').replace('#', '##')
    # try:
    fanart = re.compile('#EXTM3U').findall(link)[0]
    # except:
    #    fanart = re.compile('background=(.+?)thumb').findall(link)[0]
    # EXTINF.*,(.*)\n(https?.*.ts)
    match = re.compile(ur'#EXTINF.*,.*\nhttps?.*.ts').findall(link)
    for item in match:
        print item
        # match = re.compile('type=playlistthumb=(.+?)name=(.+?)URL=(.+?)#').findall(item)
        # for thumb, name, url in match:
        #    addDir(name, url, thumb, fanart)
        match = re.compile(ur'#EXTINF.*,(.*)\n(https?.*.ts)').findall(item)
        # for name, thumb, url in match:
        for name, url in match:
            print name + '\n' + url
            addLink(name, url)
            # thumb = null
            # fanart = null
            # addLink(name, url, thumb, fanart)


def Play(url, iconimage):
    ok = True
    liz = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz)
    try:
        xbmc.Player().play(url, liz, False)
        return ok
    except:
        pass


def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    # link = link.replace('\r', '').replace('\t', '').replace('&nbsp;', '').replace('\'', '')
    response.close()
    return link


def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'):
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]

    return param


def addLink(name, url, iconimage='', fanart='', description=''):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(3) + "&name=" + urllib.quote_plus(
        name) + "&description=" + str(description)  # mode=video?
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
    liz.setInfo(type="Video", infoLabels={"Title": name, 'plot': description})
    # liz.setProperty('fanart_image', fanart)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
    return ok


def addDir(name, url, iconimage, fanart, description=''):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(1) + "&name=" + urllib.quote_plus(
        name) + "&description=" + str(description)  # mode=folder
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, 'plot': description})
    liz.setProperty('fanart_image', fanart)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok


params = get_params()
url = None
name = None
mode = None
site = None
iconimage = None
try:
    site = urllib.unquote_plus(params["site"])
except:
    pass
try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode = int(params["mode"])
except:
    pass
try:
    iconimage = urllib.unquote_plus(params["iconimage"])
except:
    pass

print "Site: " + str(site)
print "Mode: " + str(mode)
print "URL: " + str(url)
print "Name: " + str(name)

if mode == None or url == None or len(url) < 1:
    Index()
elif mode == 1:
    GetLinks(url)
elif mode == 3:
    Play(url, iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
