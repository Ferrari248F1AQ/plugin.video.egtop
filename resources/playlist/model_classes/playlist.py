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

import datetime
import os
import re
import xbmcgui
from difflib import SequenceMatcher

from lib import utils
from lib import quicknet
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
    playlist_url = None
    
    
    def __init__(self):
        """ Virtually private constructor. """
        if playlist.__instance != None:
            self.recoveryParameter()
        else:
            playlist.__instance = self
            self.recoveryParameter()


    """
    In the playlist may be several media associated to a same title. For example for a certain movie there can be an .avi
    version or a .mkv version. This method helps to delete duplicates

    """
    def deleteDuplicates(self):
        items_filtered = []
        for item in self.playlist_filtered:
            for item_filtered in items_filtered:
                item[0] = item[0].replace(' ', '')
                item_filtered[0] = item_filtered[0].replace(' ', '')
                if SequenceMatcher(None, item[0], item_filtered[0]).ratio() >= 0.50 and item[3] is "movie":
                    if item[1].endswith('.avi'):
                        item_filtered = item

        self.playlist_filtered = items_filtered
        _cache.set( "db_playlist_filtered", items_filtered, expiration=datetime.timedelta(days = expiring_days_cache))


    """
    It download from web (via http) and save into a folder a .m3u playlist

    """
    def downloadPlaylist(self, folder, url = None):
        if not url:
            url = self.playlist_url

        try:
            html = quicknet.getURL(url, maxSec=0, tidy=False)
        except:
            html = ''

        items = parse(html.split('\n'))
        valid = len(items) > 0

        if not valid:
            return False

        name = 'downloaded_playlist.m3u'
        file = os.path.join(folder, 'PL', name)
        f = sfile.file(file, 'w')
        f.write(html)
        f.close()

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
    def extractVODFromPlaylist(self, extensions):   
    
        items_filtered = []
        for item in self.playlist:
            if item[1].endswith(extensions):
                items_filtered.append(item)
                
        self.playlist_filtered = items_filtered
        _cache.set( "db_playlist_filtered", items_filtered, expiration=datetime.timedelta(days = expiring_days_cache))

        return self.playlist_filtered
        

    """
    After that playlist has been readen and VOD have been extracted, it allows to extract VOD which are conforms to specified keywords criteria

        :param filtering_keywords: List of keywords which have to been used for filtering
        :type filtering_keywords: list
        :return: A filtered list of VOD which are conforms to the specified filtering keywords
        :rtype: list
    """
    def filterVODbyKeywords(self, filtering_keywords):

        items_filtered = []
        for item in self.playlist_filtered:
            if any(filtering_keyword in re.search('group-title="(.+?)"', item[2]).group(1) for filtering_keyword in filtering_keywords):
                items_filtered.append(item)

        self.playlist_filtered = items_filtered
        _cache.set( "db_playlist_filtered", items_filtered, expiration=datetime.timedelta(days = expiring_days_cache))

        return self.playlist_filtered


    """
    After that playlist has been readen and VOD have been extracted and filtered using keywords, it allows to split VOD by kind of media (Movies, TVShow)

    """
    def filterVODbyKindOfMedia(self):
        kind_of_media_filtering_keywords = _cache.get( "db_kind_of_media_filtering_keywords")
        items_filtered = []
        for item in self.playlist_filtered:
            #general speaking each tv series show has a title of kind (tv show name INTxINT ... .extension)
            m = re.search(rex_tv_shows, item[2])
            if m and "tvshows" in kind_of_media_filtering_keywords:
                item[3] = "tvshow"
                items_filtered.append(item)
            elif not m and "movies" in kind_of_media_filtering_keywords:
                item[3] = "movie"
                items_filtered.append(item)

        self.playlist_filtered = items_filtered
        _cache.set("db_playlist_filtered", items_filtered, expiration=datetime.timedelta(days = expiring_days_cache))

    """
    It returns the list of the filtering keywords

        :return: The list of the filtering keywords
        :rtype: list
    """
    def getLanguageFilteringKeywords(self):

        return _cache.get("db_language_filtering_keywords")


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
        title_not_splitted = ''
        kind_of_media = ''

        try:
            for line in playlist:
                line = line.strip()
                if line.startswith('#EXTINF:'):
                    title_not_splitted = line.lower()
                    title  = line.split(':', 1)[-1].split(',', 1)[-1]
                    if len(title) == 0:
                        title = "Unnamed" #SJP
                else:
                    path = line.replace('rtmp://$OPT:rtmp-raw=', '')
                    if len(path) > 0 and len(title) > 0:
                        items.append([title, path, title_not_splitted, kind_of_media])
                    path  = ''
                    title = ''
                    title_not_splitted = ''
        except:
            pass

        return items



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
    It syncs the parameters from Foundation

    """
    def recoveryParameter(self):
        self.playlist = _cache.get("db_playlist")
        self.playlist_filtered = _cache.get("db_playlist_filtered")
        self.playlist_url = _cache.get("db_playlist_url")


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
            _cache.set( "db_playlist", playlist, expiration=datetime.timedelta(days = expiring_days_cache))
            self.playlist = playlist
            return True     
        else:
            _cache.set( "db_playlist", self.playlist, expiration=datetime.timedelta(days = expiring_days_cache))
            return True




    """
    It selects the kind of media to extract (Movie, TV Series or both)

        :param kind_of_media: The selected kind of media
        :type kind_of_media: list
    """
    def selectKindOfMedia(self, kind_of_media):
        list = []
        if "Movies" in kind_of_media:
            kind_of_media_keywords = ["movies"]
            list += kind_of_media_keywords
        if "TV Shows" in kind_of_media:
            kind_of_media_keywords = ["tvshows"]
            list += kind_of_media_keywords
        _cache.set( "db_kind_of_media_filtering_keywords", list, expiration=datetime.timedelta(days = expiring_days_cache))

    """
    It selects the preferred languages for media

        :param languages: The selected languages for the media
        :type languages: list
    """
    def selectLanguages(self, languages):
        filtering_keywords = []
        if "De" in languages:
            lang_keywords = ["de", "deutsch", "dutch", "ger"]
            filtering_keywords += lang_keywords
        if "En" in languages:
            lang_keywords = ["en", "english", "uk", "eng"]
            filtering_keywords += lang_keywords
        if "Fr" in languages:
            lang_keywords = ["fr", "french", "fra"]
            filtering_keywords += lang_keywords
        if "It" in languages:
            lang_keywords = ["it", "italian", "ita"]
            filtering_keywords += lang_keywords
        _cache.set( "db_language_filtering_keywords", filtering_keywords, expiration=datetime.timedelta(days = expiring_days_cache))


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
    It sets the http path of a remote playlist

        :param url: A string containing the http url of the playlist
        :type url: string
    """
    def setPlaylistUrl(self, url):

        _cache.set("db_playlist_url", url,
                   expiration=datetime.timedelta(days=expiring_days_cache))
