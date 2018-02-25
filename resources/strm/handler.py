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

from resources.strm.model_classes.strm import strm
from config import *


def createInstance():

    return strm()

def setStrmFolder():
    abs_path_folder = os.path.join(abs_main_folder, outputstrm_name_folder)
    
    strm().setStrmFolder(abs_path_folder)    

def createStrmFileFromPlaylist(playlist):
    abs_path_folder = os.path.join(abs_main_folder, outputstrm_name_folder)
    strm().deleteFilesFromFolder(abs_path_folder)
    strm().createStrmFileFromPlaylist(playlist)


def createStrmFile(name, content):
    strm().createStrmFile(name, content)

