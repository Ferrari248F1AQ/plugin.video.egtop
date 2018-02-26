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
import sys
import codecs
import glob
import xbmcgui
import pickle
import datetime

from lib import utils
from lib import sfile
from lib import simplecache

_cache = simplecache.SimpleCache()


class strm:
    __instance = None
    
    
    def __init__(self):
        if strm.__instance != None:
            pass
        else:
            strm.__instance = self

    """
    It opens a dialog window to select where .strm will be created
    """
    def selectStrmFolder(self):
        root = utils.HOME.split(os.sep, 1)[0] + os.sep
        strm_path = xbmcgui.Dialog().browse(3, "Select .strm folder", 'files', '', False, False, root)

        _cache.set( "db_strm_folder", strm_path)


    """
    It returns the selected folder for .strm files
    """
    def getStrmFolder(self):
        folder = _cache.get("db_strm_folder")

        return folder


    """
    It sets the folder where .strm files will be saved
    
        :param name: The name of the file
        :type content: The content of the file
    """    
    def setStrmFolder(self, abs_path_folder):
        os.chdir(abs_path_folder)
  
  
    """
    It creates a .strm file for each media file contained in a Playlist

      :param playlist: Playlist from which create .strm files
      :type playlist: list
    """    
    def createStrmFileFromPlaylist(self, playlist):
      for item in playlist:
          #dots and slashs deleted from file name to avoid issues during file creation
          item[0] = item[0].replace(".", " ")
          item[0] = item[0].replace("/", " ")    
          file = codecs.open(item[0][:63] + ".strm", "a+", errors = 'ignore')
          if file:
              file.write(item[1])
  
    """
    It deletes all the files into a folder
    """
    def deleteFilesFromFolder(self, path):
        fileList = os.listdir(path)
        for filename in fileList:
            item=os.path.join(path, filename)
            if os.path.isfile(item): 
                os.remove(item)
            
    """
    It creates a new .strm file
    
        :param name: The name of the file
        :type content: The content of the file
    """    
    def createStrmFile(self, name, content):
        file = open(name + ".strm", "a+")
        file.write("test")      
    
    
    """
    It reads all the lines of the Playlist and returns a list 
    
        :param path: The absolute path of the playlist
        :type path: str
        :return: A list for which each item is a list of the type [:str name_of_media, :str path_of_media] for every value cointaned in the Playlist
        :rtype: list
    """    
    def readPlaylist(self, path):    
        if not sfile.exists(path):
            return iPlaylistURL(path)

        playlist = sfile.readlines(path) 
        items = self.parse(playlist)     
        self.savePlaylist(items)
        

        return self.playlist
     
    
        
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
            _cache.set( "db_playlist", playlist, expiration=datetime.timedelta(hours=12))
            self.playlist = playlist
            return True     
        else:
            _cache.set( "db_playlist", self.playlist, expiration=datetime.timedelta(hours=12))
            return True
                       
            
    """
    After that playlist has been readen, it selects from the Playlist only media which have a media extesion contained in Type
    
        :param items: Playlist converted in a list
        :param extensions: Type of extension to be extracted from the Playlist
        :type items: list
        :param extensions: tuple
        :return: A filtered list for which each item is a list of the type [:str name_of_media, :str path_of_media] for every value cointaned in the Playlist
        :rtype: list
    """    
    def getPlaylist(self):   
        
        self.playlist = _cache.get("db_playlist")
        self.playlist_filtered = _cache.get("db_playlist_filtered")
     
        

