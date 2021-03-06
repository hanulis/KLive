# -*- coding: utf-8 -*-
import traceback, sys
import urllib, urllib2, cookielib
import time, datetime
import json 
import os
import pickle, re
import ssl

#try:
#    from html import escape  # python 3.x
#except ImportError:
#    from cgi import escape  # python 2.x

M3U_FORMAT = '#EXTINF:-1 tvg-id=\"%s\" tvg-name=\"%s\" tvg-logo=\"%s\" group-title=\"%s\",%s\n%s\n'
M3U_RADIO_FORMAT = '#EXTINF:-1 tvg-id=\"%s\" tvg-name=\"%s\" tvg-logo=\"%s\" group-title=\"%s\" radio=\"true\",%s\n%s\n'
BROAD_URL = '%s?mode=url&type=%s&id=%s'


PATH_DATA = 'data'
PATH_OUTPUT = 'output'
SLEEP_TIME = 0.01

try:
	from io import open
except:
	pass

def ReadFile(filename):
	try:
		with open(filename, "r", encoding='utf8') as f:
			data = f.read()
		f.close()
	except:
		exc_info = sys.exc_info()
		traceback.print_exception(*exc_info)
	return data

def WriteFile(filename, data ):
	try:
		with open(filename, "w", encoding='utf8') as f:
		#with open(filename, "w") as f:
			f.write( data.decode('utf8') )
		f.close()
		return
	except Exception as e:
		#print('W22:%s' % e)
		pass

	try:
		#with open(filename, "w", encoding='utf8') as f:
		with open(filename, "w") as f:
			f.write( unicode(data) )
		f.close()
		return
	except Exception as e:
		#print('W11:%s' % e)
		pass
	

def AppendEPG(filename, data ):
	#data = data.replace('&amp;', '·')
	#data = data.replace('&', '·')
	data = data.replace('&amp;', '&')
	data = data.replace('&', '&amp;')
	try:
		with open(filename, "a", encoding='utf8') as f:
			f.write( data.decode('utf8') )
		f.close()
		return
	except Exception as e:
		#print('W22:%s' % e)
		pass

	try:
		with open(filename, "a") as f:
			f.write( unicode(data) )
		f.close()
		return
	except Exception as e:
		#print('W11:%s' % e)
		pass
	

def GetFilename(filename):
	ret = filename
	try:
		import xbmc, xbmcaddon, os
		profile = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile'))
		ret = xbmc.translatePath(os.path.join( profile, ret))
		return ret
	except:
		pass

	try:
		temp = Prefs['VERSION']
		import sys, os
		ret = os.path.join( os.getcwd(), filename )
		return ret
	except:
		pass

	try:
		import sys, os
		ret = os.path.join( os.getcwd(), 'data', filename )
		#print(ret)
		return ret
	except:
		pass

def GetEpisodeNumFromTitle(title):

    ret={}

    ret['title']=title.replace('&lt;','<').replace('&gt;','>')
    ret['title']=re.sub('<.*?>',"",ret['title']).strip()

    p = re.search("<", ret['title'])

    if p:
        ret['title']=re.sub('<.*?$','',ret['title']).strip()
    # ret['title']=ret['title'].replace('<','&lt;').replace('>','&gt;')

    ret['season']='0'
    ret['episode']=None

    p = re.search(u"시즌 ?[0-9]+", ret['title'])
    if p:
        ret['title']=re.sub(u"시즌 ?[0-9]+","", ret['title']).strip()

        season=re.sub(u"[시즌|시즌 ]","",p.group()).strip()
        ret['season']=season

    p = re.search('[0-9]+'+u"[회|화|부]",ret['title'])
    if p:
        ret['title']=re.sub('[0-9]+'+u"[회|화|부]","", ret['title']).strip()
        ret['title']=re.sub(r'\(.*?\)',"",ret['title']).strip()

        episode=re.sub(u"[회|화|부]","",p.group()).strip()
        ret['episode']=episode

        return ret

    ret['title']=re.sub(r'\(.*?\)',"",ret['title']).strip()
    return ret
