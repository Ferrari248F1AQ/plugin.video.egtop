﻿# -*- coding: utf-8 -*-
import os
import sys
import inspect
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib
import urlparse
import datetime


import resources.playlist.handler as handlerPlaylist
import resources.strm.handler as handlerStrm

#imports config parameters
from config import *

sys.path.insert(0, parent_abs_main_folder)

# plugin constants
__name_plugin__ = "EgTop"
__plugin__ = "plugin.video.egtop"
__author__ = "Ferrari248F1AQ"

Addon = xbmcaddon.Addon(id=__plugin__)

# plugin handle
handle = int(sys.argv[1])

# utility functions
def parameters_string_to_dict(parameters):
    ''' Convert parameters encoded in a URL to a dict. '''
    paramDict = dict(urlparse.parse_qsl(parameters[1:]))
    return paramDict
    
def addDirectoryItem(parameters, li):
    url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    return xbmcplugin.addDirectoryItem(handle=handle, url=url, 
        listitem=li, isFolder=True)
        
def localPlaylist():
    import playlist
    playlist = playlist.getPlaylist()

    if not playlist:
        return False

    return True

# UI builder functions
def show_root_menu():
    ''' Show the plugin root menu '''
    liStyle = xbmcgui.ListItem("1) Aggiungi M3U")
    addDirectoryItem({"mode": "aggiungi_lista_m3u"}, liStyle)
    liStyle = xbmcgui.ListItem("2) Crea .strm files")
    addDirectoryItem({"mode": "crea_strm"}, liStyle)
    liStyle = xbmcgui.ListItem("DEBUG")
    addDirectoryItem({"mode": "debug"}, liStyle)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

    

# parameter values
params = parameters_string_to_dict(sys.argv[2])
# TODO: support content_type parameter, provided by XBMC Frodo.
content_type = str(params.get("content_type", ""))
mode = str(params.get("mode", ""))
behaviour = str(params.get("behaviour", ""))
url = str(params.get("url", ""))
date = str(params.get("date", ""))
channelId = str(params.get("channel_id", ""))
index = str(params.get("index", ""))
pathId = str(params.get("path_id", ""))
subType = str(params.get("sub_type", ""))
tags = str(params.get("tags", ""))


if mode == "aggiungi_lista_m3u":
    playlist = handlerPlaylist.createInstance()
    handlerPlaylist.openLocalPlaylist()
    extensions = ('.avi', '.mkv')
    playlist_filtered = handlerPlaylist.extractVODFromPlaylist(extensions)
    xbmcgui.Dialog().ok(str(__name_plugin__), "Playlist added! It will be recorded for " + str(expiring_days_playlists) + " days.")   
    
if mode == "crea_strm":
    handlerStrm.setStrmFolder()
    playlist = handlerPlaylist.getPlaylistFiltered()
    handlerStrm.createStrmFileFromPlaylist(playlist)
    xbmcgui.Dialog().ok(str(__name_plugin__), "All .strm files created!")
    
if mode == "debug":
    from lib import simplecache

    _cache = simplecache.SimpleCache()
    
    xbmcgui.Dialog().ok("mammota", str(_cache.get("db_playlist")) ) 
    """
    from lib import simplecache

    _cache = simplecache.SimpleCache()
       
    if _cache.set( "testare", "porco_dincisss", expiration=datetime.timedelta(hours=12)):
        xbmcgui.Dialog().ok("mammota", "mammota" )
    else:
        xbmcgui.Dialog().ok("mammota", _cache.get("db_playlist") ) 
    """       

else:
    show_root_menu()
