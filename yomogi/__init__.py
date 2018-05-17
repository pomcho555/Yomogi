import sys
import os
import configparser
config = configparser.ConfigParser()
INI_FILE = './config.ini'
INI_FILE = 'config.ini'
ANALYZER = 'MeCab'
TAGGER = ''
LANG = 'JP'

path = os.path.dirname(__file__) + '/' + INI_FILE
if os.path.exists(path):
    config.read(path, encoding='utf-8')
    ANALYZER = config.get('settings', 'analyzer')
    TAGGER = config.get('settings', 'tagger')
    LANG = config.get('settings', 'LANG')
else:
    print('%s is not found' % INI_FILE)
    #sys.stderr.write('%s is not found' % INI_FILE)
    #sys.exit(2)

from importlib import import_module
#import analyzer dynamically
Analyzer = import_module(ANALYZER)
from .Yomogi import *
from .word_divider import WordDivider
from .normalize_neologd import *
