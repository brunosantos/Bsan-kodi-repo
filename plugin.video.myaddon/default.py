import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

my_addon = xbmcaddon.Addon()
my_setting = my_addon.getSetting('my_setting') # returns the string 'true' or 'false'
my_addon.setSetting('my_setting', 'false')

xbmcplugin.setContent(addon_handle, 'movies')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)

if mode is None:
    url = build_url({'mode': 'folder', 'foldername': 'Folder One'})
    li = xbmcgui.ListItem('Folder One', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    url = build_url({'mode': 'folder', 'foldername': 'Folder Two'})
    li = xbmcgui.ListItem('Folder Two', iconImage='DefaultFolder.png')
    #li.setProperty('fanart_image', my_addon.getAddonInfo('fanart'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'folder':
    foldername = args['foldername'][0]
    url = 'http://localhost/some_video.mkv'
    li = xbmcgui.ListItem(foldername + ' Video', iconImage='DefaultVideo.png')
    li.setProperty('fanart_image', 'fanartb.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)
    
    
    