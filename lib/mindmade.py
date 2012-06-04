'''
Created on Jul 18, 2011

@author: andi
'''

__all__ = [ "log", "notify", "htmldecode", "fetchHttp" ]

import os, re
import urllib, urllib2, HTMLParser
import datetime
import xbmc, xbmcaddon

addon = xbmcaddon.Addon()
LOGFILE = os.path.join( addon.getAddonInfo('path'), "log.txt");

entitydict = { "E4": u"\xE4", "F6": u"\xF6", "FC": u"\xFC",
               "C4": u"\xE4", "D6": u"\xF6", "DC": u"\xDC",
               "2013": u"\u2013"}


def log( msg):
    msg = msg.encode( "latin-1")
    logf = open( LOGFILE, "a")
    logf.write( "%s: " % datetime.datetime.now().strftime( "%Y-%m-%d %I:%M:%S"))
    logf.write( msg)
    logf.write( '\n')
    logf.close()
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

def fetchHttp( url, args={}, hdrs={}, post=False):
    log("fetchHttp(%s): %s" % ("POST" if post else "GET", url))
    hdrs["User-Agent"] = "Mozilla/5.0 (X11; Linux i686; rv:5.0) Gecko/20100101 Firefox/5.0"
    if post:
        req = urllib2.Request( url, urllib.urlencode( args), hdrs)
    else:
	url = url + "?" + urllib.urlencode( args)
	req = urllib2.Request( url, None, hdrs)
    response = urllib2.urlopen( req)
    encoding = re.findall("charset=([a-zA-Z0-9\-]+)", response.headers['content-type'])
    text = response.read()
    if len(encoding):
        responsetext = unicode( text, encoding[0] );
    else:
        responsetext = text
    response.close()

    return responsetext
