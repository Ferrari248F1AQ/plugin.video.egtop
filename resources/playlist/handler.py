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

def createInstance():

    return playlist()

def openLocalPlaylist():
    path = playlist().selectLocalPlaylist()
    items = playlist().readPlaylist(path)

    return items
    
    
def extractVODFromPlaylist(extensions):
    items = playlist().extractVODFromPlaylist(extensions)
    return items

    
def getPlaylist():
    plylst = playlist().getPlaylist()

    return plylst

def getPlaylistFiltered():
    plylst = playlist().getPlaylistFiltered()

    return plylst