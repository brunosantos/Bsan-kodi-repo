import sys
import urllib2
from default import activado, mensagemok, net
from resources.lib.daring import user_agent


def abrir_url(url,erro=True):
    if url.startswith('sTA,'):
        from resources.lib import cloudflare
        return cloudflare.cleaner(url)
    try:
        print "A fazer request normal de: " + url
        req = urllib2.Request(url)
        req.add_header('User-Agent', user_agent)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link
    except urllib2.HTTPError, e:
        if erro==True and activado==False:
            host='http://' + url.split('/')[2]
            mensagemok('TV Portuguesa',str(urllib2.HTTPError(e.url, e.code, "Erro na página.", e.hdrs, e.fp)),'Verifique manualmente se a página está operacional.',host)
            sys.exit(0)
    except urllib2.URLError, e:
        if erro==True and activado==False:
            mensagemok('TV Portuguesa',"Erro na página. Verifique manualmente",'se a página está operacional. ' + url)
            sys.exit(0)


def abrir_url_cookie(url,erro=True,forcedns=False):
    print "A fazer request com cookie de: " + url
    try:
        if forcedns==False:
            hdr = {'User-Agent': user_agent, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
            req = urllib2.Request(url, headers=hdr)
            page = urllib2.urlopen(req)
            content = page.read()
            return content
        else:
            from resources.lib import dnsrequest
            content=dnsrequest.request(url)
            return content
    except urllib2.HTTPError, e:
        if erro==True and activado==False:
            host='http://' + url.split('/')[2]
            mensagemok('TV Portuguesa',str(urllib2.HTTPError(e.url, e.code, "Erro na página.", e.hdrs, e.fp)),'Verifique manualmente se a página está operacional.',host)
            sys.exit(0)
    except urllib2.URLError, e:
        if erro==True and activado==False:
            host='http://' + url.split('/')[2]
            mensagemok('TV Portuguesa',"Erro na página. Verifique manualmente",'se a página está operacional.',host)
            sys.exit(0)


def abrir_url_tommy(url,referencia,form_data=None,erro=True,forcedns=False):
    print "A fazer request tommy de: " + url
    #method 1
    try:
        if form_data==None:
            if forcedns==False:
                link = net.http_GET(url,referencia).content
            else:
                from resources.lib import dnsrequest
                link=dnsrequest.request(url)
        else:link= net.http_POST(url,form_data=form_data,headers=referencia).content.encode('latin-1','ignore')
        return link
    #method 2
    #try:
    #    if form_data==None:link = requests.get(url,headers=referencia).text
    #    else:link= requests.post(url,params=form_data,headers=referencia).text
    #    return link

    except urllib2.HTTPError, e:
        if erro==True and activado==False:
            host='http://' + url.split('/')[2]
            mensagemok('TV Portuguesa',str(urllib2.HTTPError(e.url, e.code, "Erro na página.", e.hdrs, e.fp)),'Verifique manualmente se a página está operacional.',host)
            sys.exit(0)
    except urllib2.URLError, e:
        if erro==True and activado==False:
            host='http://' + url.split('/')[2]
            mensagemok('TV Portuguesa',"Erro na página. Verifique manualmente",'se a página está operacional. ' + host)
            sys.exit(0)


