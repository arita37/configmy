# pylint: disable=redefined-builtin
r"""
.. module::  configmy
   :platform: Unix, Windows
   :synopsis: Generic interface to loaders for various config file formats.

- Home: 
- (Latest) Doc:
- PyPI: 
- Copr RPM repos: 

"""
#from .globals import AUTHOR, VERSION
#from .api import (
#    single_load, multi_load, load, loads, dump, dumps, validate, gen_schema,
#    list_types, find_loader, merge, get, set_, open,
#    MS_REPLACE, MS_NO_REPLACE, MS_DICTS, MS_DICTS_AND_LISTS,
#    UnknownParserTypeError, UnknownFileTypeError
#)

__author__ = "Kevin"
#__version__ = "0.12.2"


from . import configmy
__all__ = ['get', 'set', 'get_environ_details']

# print(__file__)
# vim:sw=4:ts=4:et:


from .configmy import get, set,  get_environ_details,  get_config_from_environ, zdoc, ztest



#from .configmy import *





'''
import configmy

import os
for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    __import__(module[:-3], locals(), globals())
del module, os
'''




