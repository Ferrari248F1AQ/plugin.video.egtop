import os
import sys
import inspect

#
abs_main_folder = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

parent_abs_main_folder = os.path.dirname(abs_main_folder)

rex_tv_shows = r'(\d+)x(\d+)|(s\d+\se\d+)'

outputstrm_name_folder = "output"

expiring_days_cache = 2000
#
