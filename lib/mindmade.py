'''
Created on Jul 18, 2011

@author: andi
'''

__all__ = [ "log", "notify", "htmldecode", "fetchHttp",
            "getUID", "getPersistent", "setPersistent", "sayHi"]

import os, re, time
import threading
import urllib, urllib2, HTMLParser
import datetime
import uuid

import xbmc, xbmcaddon
import simplejson as json

addon = xbmcaddon.Addon()
LOGFILE = os.path.join( addon.getAddonInfo('path'), "resources", "log.txt");
DATAFILE = os.path.join( addon.getAddonInfo('path'), "resources", "data.json");

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
    log( "fetchHttp(%s): %s" % ("POST" if post else "GET", url))
    if args: log( "args-keys: %s" % args.keys())
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


def getPersistent( key, default = None):
    if not os.path.exists( DATAFILE): return default
    data = json.load( file( DATAFILE, "r"))
    if key in data.keys():
        return data[key]
    return default

def setPersistent( key, value):
    if os.path.exists( DATAFILE): 
        data = json.load( file( DATAFILE, "r"))
    else:
        data = dict();
    
    data[key] = value
    json.dump( data, file( DATAFILE, "w"))
    
def getUID():
    uid = getPersistent( "uid")
    if not uid:
        uid = str( uuid.uuid1())
    setPersistent( "uid", uid)
    return uid

def _sendhome( data):
    from jsonrpc import ServiceProxy
    homeurl = "http://www.mindmade.org/~andi/research/python/server.py"
    proxy = ServiceProxy( homeurl)
    result = proxy.log( data)
    log( "result %s" % result)

def sayHi():
    HI_PERIOD = 60 * 60 * 6     # actions within 6 hours are treated as one session
    lastusage = getPersistent( "lastusage", 0)
    now = int( time.time())
    if now - lastusage > HI_PERIOD:
        usagecount = getPersistent( "usagecount", 0)
        usagecount += 1
        uid = getUID()
        addonid = addon.getAddonInfo( "id")
        version = addon.getAddonInfo( "version")
        logparams = { "userid": uid, "addon": addonid, "version": version, "usagecount": usagecount}
        t = threading.Thread( target=_sendhome, args=(logparams,))
        t.setDaemon( True)
        t.start()
        
        setPersistent( "lastusage", now)
        setPersistent( "usagecount", usagecount)
