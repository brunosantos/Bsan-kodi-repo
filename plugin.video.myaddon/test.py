import urllib, urllib2, os, re, sys


def Index():
    GetLinks('https://dl.dropboxusercontent.com/s/35q79t3m9cwuqdj/tvdasograv2.m3u')


def GetLinks(url):
    link = open_url(url)
    path = "C:\\raspberrypi\\Bsan-kodi-repo\\plugin.video.myaddon\\resources\data\\feed.m3u"
    link2 = readFromCache(path)
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
    link = link.replace('\r', '').replace('\t', '').replace('&nbsp;', '').replace('\'', '')
    response.close()
    return link


def readFromCache(path):
    with open(path, "r") as m3ufile:
        data = m3ufile.read().replace('\n', '')
        return data


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


Index()
