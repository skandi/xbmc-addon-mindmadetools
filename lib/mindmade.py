'''
Created on Jul 18, 2011

@author: andi
'''

__all__ = [ "log", "notify", "htmldecode", "fetchHttp" ]

import re
import urllib, urllib2, HTMLParser
import xbmc


entitydict = { "E4": u"\xE4", "F6": u"\xF6", "FC": u"\xFC",
               "C4": u"\xE4", "D6": u"\xF6", "DC": u"\xDC",
               "2013": u"\u2013"}


def log( msg):
    xbmc.log("### %s" % msg, level=xbmc.LOGNOTICE)

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

def fetchHttp( url, args={}, hdrs={}):
    log("fetchHttp " + url)
    url = url + "?" + urllib.urlencode( args) 
    hdrs["User-Agent"] = "Mozilla/5.0 (X11; Linux i686; rv:5.0) Gecko/20100101 Firefox/5.0"

    req = urllib2.Request( url, urllib.urlencode( args), hdrs)
    response = urllib2.urlopen( req)
    encoding = re.findall("charset=([a-zA-Z0-9\-]+)", response.headers['content-type'])
    text = response.read()
    if len(encoding):
        responsetext = unicode( text, encoding[0] );
    else:
        responsetext = text
    response.close()
    return responsetext
