#
#       Copyright (C) 2018-
#       Emanuele Guardiani (@ferrari248f1aq)
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with XBMC; see the file COPYING.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#

import xbmc
import os
import glob
import xbmcgui
import pickle
import datetime

from lib import utils
from lib import sfile
from lib import simplecache

from config import *

_cache = simplecache.SimpleCache()


PLAYLIST_EXT= '.m3u|.m3u8'

class playlist:
    __instance = None

    playlist_path = None
    playlist = None
    playlist_filtered = None
    
    
    def __init__(self):
        """ Virtually private constructor. """
        if playlist.__instance != None:
            self.recoveryParameter()
        else:
            playlist.__instance = self
            self.recoveryParameter()

    """
    It opens a dialog window to select a Playlist in a local path
    """
    def selectLocalPlaylist(self):
        root     = utils.HOME.split(os.sep, 1)[0] + os.sep    
        playlist_path = xbmcgui.Dialog().browse(1, utils.GETTEXT(30148), 'files', PLAYLIST_EXT, False, False, root)
    
        if playlist and playlist != root:
            self.playlist_path = playlist
            return playlist_path

        return None
    

    """
    It reads all the lines of the Playlist and returns a list 
    
        :param path: The absolute path of the playlist
        :type path: str
        :return: A list for which each item is a list of the type [:str name_of_media, :str path_of_media] for every value cointaned in the Playlist
        :rtype: list
    """    
    def readPlaylist(self, path):    
        if not sfile.exists(path):
            pass

        playlist = sfile.readlines(path) 
        items = self.parse(playlist)   
        self.savePlaylist(items)
        

        return self.playlist
     
            
    """
    It converts every media contained in the Playlist list for which each item 
    is a list of the type [:str name_of_media, :str path_of_media] for every value cointaned in the Playlist
    
        :param playlist: The playlist
        :type playlist: sfile
        :return: A list for which each item is a list of the type [:str name_of_media, :str path_of_media] for every value cointaned in the Playlist
        :rtype: list
    """          
    def parse(self, playlist):
        if len(playlist) == 0:
            return []

        items = []
        path  = ''
        title = ''
 
        try:
            for line in playlist:         
                line = line.strip()
                if line.startswith('#EXTINF:'):                
                    title  = line.split(':', 1)[-1].split(',', 1)[-1]
                    if len(title) == 0:
                        title = "Unnamed" #SJP
                else:
                    path = line.replace('rtmp://$OPT:rtmp-raw=', '')
                    if len(path) > 0 and len(title) > 0:                    
                        items.append([title, path])
                    path  = ''
                    title = ''
        except:
            pass  
          
        return items    

    """
    After that playlist has been readen, it selects from the Playlist only media which have a media extesion contained in Type
    
        :param items: Playlist converted in a list
        :param extensions: Type of extension to be extracted from the Playlist
        :type items: list
        :param extensions: tuple
        :return: A filtered list for which each item is a list of the type [:str name_of_media, :str path_of_media] for every value cointaned in the Playlist
        :rtype: list
    """    
    def extractVODFromPlaylist(self, extensions):   
    
        items_filtered = []
        for item in self.playlist:
            if item[1].endswith(extensions):
                items_filtered.append(item)
                
        self.playlist_filtered = items_filtered
        _cache.set( "db_playlist_filtered", items_filtered, expiration=datetime.timedelta(hours=12))        

        return self.playlist_filtered
        
        
        
    """
    After that playlist has been readen, it selects from the Playlist only media which have a media extesion contained in Type
    
        :param items: Playlist converted in a list
        :param extensions: Type of extension to be extracted from the Playlist
        :type items: list
        :param extensions: tuple
        :return: A filtered list for which each item is a list of the type [:str name_of_media, :str path_of_media] for every value cointaned in the Playlist
        :rtype: list
    """    
    def savePlaylist(self, playlist = None): 
        if playlist: 
            _cache.set( "db_playlist", playlist, expiration=datetime.timedelta(days = expiring_days_playlists))
            self.playlist = playlist
            return True     
        else:
            _cache.set( "db_playlist", self.playlist, expiration=datetime.timedelta(days = expiring_days_playlists))
            return True
    
    """
    It syncs the parameters with Foundation 

    """    
    def recoveryParameter(self):
        self.playlist = _cache.get("db_playlist") 
        self.playlist_filtered = _cache.get("db_playlist_filtered")    
             
            
    """
    It returns the Playlist
    
        :return: The Playlist
        :rtype: list
    """    
    def getPlaylist(self):   
        
        return _cache.get("db_playlist")
     
    """
    It returns the Playlist filtered by media elements
    
        :return: The Playlist filtered by media elements
        :rtype: list
    """    
    def getPlaylistFiltered(self):   
        
        return _cache.get("db_playlist_filtered")  

