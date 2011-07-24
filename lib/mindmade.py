'''
Created on Jul 18, 2011

@author: andi
'''

__all__ = [ "log", "notify", "htmldecode", "fetchHttp" ]

import re
import urllib2, HTMLParser
import xbmc


entitydict = { "E4": u"\xE4", "F6": u"\xF6", "FC": u"\xFC",
               "C4": u"\xE4", "D6": u"\xF6", "DC": u"\xDC",
               "2013": u"\u2013"}


def log( msg):
    xbmc.output("### %s" % msg, level=xbmc.LOGNOTICE)

def notify( title, message):
    xbmc.executebuiltin("XBMC.Notification("+title+","+message+")")

def htmldecode( s):
    try:
        h = HTMLParser.HTMLParser()
        s = h.unescape( s)
        for k in entitydict.keys():
            s = s.replace( "&#x" + k + ";", entitydict[k])
    except UnicodeDecodeError:
        pass
        
    return s

def fetchHttp( url):
    log("fetchHttp " + url)
    hdrs = {
        "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3",
    }

    req = urllib2.Request( url, headers=hdrs)
    response = urllib2.urlopen( req)
    encoding = re.findall("charset=([a-zA-Z0-9\-]+)", response.headers['content-type'])
    text = response.read()
    if len(encoding):
        responsetext = unicode( text, encoding[0] );
    else:
        responsetext = text
    response.close()
#    return responsetext.encode("utf-8")
    return responsetext
