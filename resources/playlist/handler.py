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
import xbmcgui

from resources.playlist.model_classes.playlist import playlist


def openLocalPlaylist():
    path = playlist().selectLocalPlaylist()
    items = playlist().readPlaylist(path)

    return items
    
    
def extractVODFromPlaylist():
    extensions = ('.avi', '.mkv')
    items = playlist().extractVODFromPlaylist(extensions)

    return items

def filterVODbyKindOfMedia():
    playlist().filterVODbyKindOfMedia()


def filterVODbyLanguage():
    filtering_keywords = playlist().getLanguageFilteringKeywords()
    playlist().filterVODbyKeywords(filtering_keywords)


def getFilteringKeywords():
    filtering_keywords = playlist().getFilteringKeywords()
    playlist().filterVODbyKeywords(filtering_keywords)

    
def getPlaylist():
    plylst = playlist().getPlaylist()

    return plylst

def getPlaylistFiltered():
    plylst = playlist().getPlaylistFiltered()

    return plylst

def selectKindOfMedia():
    list_kind_of_media = xbmcgui.Dialog().multiselect("Select kind of Media", ["Movies", "TV Series"])
    kind_of_media = []
    if 0 in list_kind_of_media:
        kind_of_media.append("Movies")
    if 1 in list_kind_of_media:
        kind_of_media.append("TV Shows")
    playlist().selectKindOfMedia(kind_of_media)


def selectLanguages():
    list_sel_lang = xbmcgui.Dialog().multiselect("Select media language", ["De", "En", "Fr", "It"])
    languages = []
    if 0 in list_sel_lang:
        languages.append("De")
    if 1 in list_sel_lang:
        languages.append("En")
    if 2 in list_sel_lang:
        languages.append("Fr")
    if 3 in list_sel_lang:
        languages.append("It")
    playlist().selectLanguages(languages)
