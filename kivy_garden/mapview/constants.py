import os
import platform
MIN_LATITUDE = -90.0
MAX_LATITUDE = 90.0
MIN_LONGITUDE = -180.0
MAX_LONGITUDE = 180.0
if platform.system() == 'Darwin':
    CACHE_DIR = os.getenv("HOME") + '/Library/Low-Fuel/'
if platform.system() == 'Linux':
    CACHE_DIR = '/tmp/Low-Fuel/'
if platform.system() == 'Windows':
    CACHE_DIR = os.getenv("LOCALAPPDATA") + '\\Temp\\Low-Fuel\\' 
