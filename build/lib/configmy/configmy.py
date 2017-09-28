# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from importlib import import_module
from pkgutil import walk_packages
import builtins, operator, inspect, future
import pandas as pd, regex, past, ast, re, math,  os, sys, glob
import platform

from collections import OrderedDict
from attrdict import AttrDict as dict2


####################################################################################################
__path__= '/'
#__version__= "1.0.0"
__file__= "configmy.py"
__all__ = ['get_environ_details', 'get_config_from_environ', 'get', 'set']


CONFIGMY_ROOT_FILE= "CONFIGMY_ROOT_FILE"



def zdoc() :
 print('''
#Test
from configmy import configmy
configmy.get("configmy/ztest/test_config.py", output= ["_CFG", "DIRCWD",])

CFG, DIRCWD= configmy.get("configmy/ztest/test_config.py", output= ["_CFG", "DIRCWD",])

configmy.set( "D:/_devs/Python01/project27/github/configmy/configmy/ztest/test_config.py") 

configmy.set("D:/_devs/Python01/project27/__config/CONFIGMY_ROOT_FILE.py")


#Usage
import configmy; CFG, DIRCWD= configmy.get(output= ["_CFG", "DIRCWD"]);
 CFG, DIRCWD

''')



####################################################################################################
def get_environ_details(isprint=0):
 '''
  Calculate environnment details
  platform.system() #returns the base system, in your case Linux
  platform.release() #returns release version
  Dynamic release
 '''
 CFG   = {'os': sys.platform[:3],
          'username': os.path.expanduser('~').split("\\")[-1].split("/")[-1],
          "pythonversion":      str(sys.version_info.major),
          "pythonversion_full": str(sys.version_info),
          'os_release' :        str(platform.release())
          }

 if isprint :  print(CFG); return CFG
 else :
   # CFG= dict2(CFG);        
   return CFG



def get_config_from_environ(CFG, dd_config_all, method0=["os", "username"]):
    '''
    Create unique id from method, using environnment details
    :param CFG: 
    :param dd_config_all: 
    :param method0:    method specify in os release, os, username, 
     method0=["os_", "username_"]  :           "win+MyUser1'    
     method0=["os_", "username_", "test"]  :   "win+MyUser1+test'
     method0=["os_", "username_", "prod"]  :   "win+MyUser1+prod'
     
     Order of preference :
       1) argument method0
       2) CONFIGMY_ROOT_FILE["configmy"]["method0"]
       3) Default method os_username    
    '''

    #Check configmy_root_file for method0
    method_default= "os_username"
    if "_".join(method0) == method_default :
       try :     method0= dd_config_all["configmy"]["method0"]
       except :  pass


    config_unique_id= ""   #  os_env_id
    for x in method0 :
       try :     key= str(CFG[x])
       except :  key= x

       if config_unique_id == "": config_unique_id= key
       else :                     config_unique_id=  config_unique_id + "+" + key

    dd_config= dd_config_all[config_unique_id]
    return dd_config



def get(config_file="_ROOT", method0=["os", "username"], output=["_CFG", "DIRCWD",]):
    ''' Get the config dictionary.
    method0:       os, username, pythonversion  
    config_file:  _ROOT: os.environ["CONFIGMY_ROOT_FILE"]  /   CONFIGMY_ROOT_FILE.py
    outputs:      _ALL: full file, _CFG : Config File,  DIRCWD root directory 
    '''
    try :
        if config_file == "_ROOT" :  config_file= os.environ[CONFIGMY_ROOT_FILE]
    except Exception as e :
        print(e);  print("Cannot Find os.environ['CONFIGMY_ROOT_FILE'] ")
        return None


    try :
      with   open(config_file) as f1 :
        dd_config_all = ast.literal_eval(f1.read())
    except Exception as e:
      print(e) ;   print("Incorrect config file Dictionnary format")
      return None


    CFG=       get_environ_details()
    dd_config= get_config_from_environ(CFG, dd_config_all, method0=method0)
    dd_config= dict2(dd_config)


    ######################################################################
    output_tuple= ()
    for x in output :
      if x[0] != "_" :  output_tuple= (output_tuple + (dd_config[x],) )   #Ask directly items argument
      if x == "_CFG" :  output_tuple= (output_tuple + (dd_config,))
      if x == "_ALL" :  output_tuple= (output_tuple + (dd_config_all,))

    return output_tuple



def os_file_replacestring1(findStr, repStr, filePath):
    "replaces all findStr by repStr in file filePath"
    import fileinput
    file1= fileinput.FileInput(filePath, inplace=True, backup='.bak')
    for line in file1:
       line= line.replace(findStr,  repStr)
       sys.stdout.write(line)
    file1.close()
    print(("OK: "+format(filePath)))



def set(configmy_root_file="") :
    '''
    Do Command Line to set configmy root file in   os.environ['CONFIGMY_ROOT_FILE'] 
    '''
    CFG=      get_environ_details(isprint=0)
    env_var = CONFIGMY_ROOT_FILE

    os.environ[env_var] = configmy_root_file # visible in this process + all children

    if CFG["os"] == "win" :
      os.system("SETX {0} {1} /M".format(env_var, configmy_root_file))
      os.system("SETX {0} {1} ".format(env_var, configmy_root_file))
      print("You need to reboot Windows to get the Env Var visible, Permanently")


    if CFG["os"] == "lin" :
      with open(os.path.expanduser("~/.bashrc"), "a") as outfile:
         outfile.write("export  "+env_var + "="+configmy_root_file)

    if CFG["os"] == "mac" :
       pass



def  ztest():
   import configmy
   path= configmy.__path__[0]
   configmy.get(path+"/ztest/test_config.py", output= ["_CFG", "DIRCWD",])

   # configmy.set(path+"/ztest/test_config.py")
   configmy.get(method0=["os", "username"], output=["_CFG", "DIRCWD"] )







###############################################################################################
global IIX; IIX=0
def pprint(a): global IIX; IIX+= 1; print("\n--" + str(IIX) + ": " + a, flush=True)

if __name__ == "__main__"  :
  import argparse
  ppa = argparse.ArgumentParser()
  ppa.add_argument('--action', type=str, default= ''  ,       help=" unit_test")
  ppa.add_argument('--module', type=str, default= ''  ,       help=" unit_test")
  arg = ppa.parse_args()



if __name__ == "__main__" and  arg.action != ''  and  arg.module != '' :
    print("Running Task")
    globals()[arg.action](arg.module)   #Execute command



if __name__ == "__main__" and  arg.action == 'test' :
    pprint('### Unit Tests')
    #os_folder_create("/ztest")
    import configmy

    pprint("get")
    configmy.ztest()






















'''
import configmy; CFG, DIRCWD= configmy.a.get()


print(configmy)



Open terminal window and change directory to /project/
  python setup.py sdist bdist_wheel --universal
  twine upload dist/*



5) Build and upload subsequent updates to pypi
Update the change log and edit the version number in setup.py and package/__init__.py.

Open terminal window and change directory to /project/

  python setup.py sdist bdist_wheel --universal
  twine upload dist/*



'''


'''
import os, sys
CFG   = {'plat': sys.platform[:3]+"-"+os.path.expanduser('~').split("\\")[-1].split("/")[-1], "ver": sys.version_info.major}
DIRCWD= {'win-asus1': 'D:/_devs/Python01/project27/', 'win-unerry': 'G:/_devs/project27/' , 'lin-noel': '/home/noel/project27/', 'lin-ubuntu': '/home/ubuntu/project27/' }
try :
  # DIRCWD= os.environ["DIRCWD"];
  from attrdict import AttrDict as dict2
  DIRCWD= DIRCWD[ CFG["plat"]]; # print(DIRCWD, flush=True)
  os.chdir(DIRCWD); sys.path.append(DIRCWD + '/aapackage')
  f= open(DIRCWD+'/__config/config.py'); CFG= dict2(dict(CFG,  **eval(f.read()))); f.close()  #Load Config
  # print(CFG.github_login, flush=True)
except :  print("Project Root Directory unknown")

execfile( DIRCWD + '/aapackage/coke_functions.py')


method_blocked= {'__builtins__':None}
method_allowed

eval('[1, cpu_count()]', method_blocked, {})

import ast
ast.literal_eval(node_or_string)



>>>from os import cpu_count
>>>exposed_methods = {'cpu_count': cpu_count}
>>>eval('cpu_count()', {'__builtins__':None}, exposed_methods)
8
>>>eval('abs(cpu_count())', {'__builtins__':None}, exposed_methods)
TypeError: 'NoneType' object is not subscriptable


'''




'''





https://gist.github.com/gboeing/dcfaf5e13fad16fc500717a3a324ec17


Set up pypi
Create a file in the home directory called ~/.pypirc with contents:
[distutils]
index-servers = pypi



[pypi]
repository = https://pypi.python.org/pypi
username = YourPyPiUsername
password = YourPyPiPassword
Build, register, and upload to pypi



Open terminal window and change directory to /project/
Then run setup.py with sdist to build a source distribution and bdist_wheel to build a wheel (with --universal flag if your package is Python 2/3 universal). Then use twine to register it and upload to pypi.
python setup.py sdist bdist_wheel --universal
twine register dist/project-x.y.z.tar.gz
twine register dist/mypkg-0.1-py2.py3-none-any.whl
twine upload dist/*
Build and upload subsequent updates to pypi







Update the change log and edit the version number in setup.py and package/__init__.py.
Open terminal window and change directory to /project/ then run setup.py with sdist to build a source distribution and bdist_wheel to build a wheel (with --universal flag if your package is Python 2/3 universal). Remove old versions from /project/dist/ and then use twine to upload to pypi.
python setup.py sdist bdist_wheel --universal
twine upload dist/*



Release your code on GitHub
To tag your current commit as a released version, run:

git tag -a v0.1 -m "annotation for this release"
git push origin --tags






'''








####################################################################################################





def obj_is_iterable(obj):
    """
    >>> is_iterable([])
    True
    >>> is_iterable(())
    True
    >>> is_iterable([x for x in range(10)])
    True
    >>> is_iterable((1, 2, 3))
    True
    >>> g = (x for x in range(10))
    >>> is_iterable(g)
    True
    >>> is_iterable("abc")
    False
    >>> is_iterable(0)
    False
    >>> is_iterable({})
    False
    """
    return isinstance(obj, (list, tuple, types.GeneratorType)) or \
        (not isinstance(obj, (int, str, dict)) and
         bool(getattr(obj, "next", False)))


def np_list_concat(xss):
    """
    Concatenates a list of lists.

    >>> concat([[]])
    []
    >>> concat((()))
    []
    >>> concat([[1,2,3],[4,5]])
    [1, 2, 3, 4, 5]
    >>> concat([[1,2,3],[4,5,[6,7]]])
    [1, 2, 3, 4, 5, [6, 7]]
    >>> concat(((1,2,3),(4,5,[6,7])))
    [1, 2, 3, 4, 5, [6, 7]]
    >>> concat(((1,2,3),(4,5,[6,7])))
    [1, 2, 3, 4, 5, [6, 7]]
    >>> concat((i, i*2) for i in range(3))
    [0, 0, 1, 2, 2, 4]
    """
    return list(anyconfig.compat.from_iterable(xs for xs in xss))




# _LIST_LIKE_TYPES = (collections.Iterable, collections.Sequence)


def obj_is_dict_like(obj):
    """
    :param obj: Any object behaves like a dict.

    >>> is_dict_like("a string")
    False
    >>> is_dict_like({})
    True
    >>> is_dict_like(anyconfig.compat.OrderedDict((('a', 1), ('b', 2))))
    True
    """
    return isinstance(obj, (dict, collections.Mapping))  # any others?


def obj_is_namedtuple(obj):
    """
    >>> p0 = collections.namedtuple("Point", "x y")(1, 2)
    >>> is_namedtuple(p0)
    True
    >>> is_namedtuple(tuple(p0))
    False
    """
    return isinstance(obj, tuple) and hasattr(obj, "_asdict")


def obj_is_list_like(obj):
    """
    >>> is_list_like([])
    True
    >>> is_list_like(())
    True
    >>> is_list_like([x for x in range(10)])
    True
    >>> is_list_like((1, 2, 3))
    True
    >>> g = (x for x in range(10))
    >>> is_list_like(g)
    True
    >>> is_list_like("abc")
    False
    >>> is_list_like(0)
    False
    >>> is_list_like({})
    False
    """
    return isinstance(obj, _LIST_LIKE_TYPES) and \
        not (isinstance(obj, anyconfig.compat.STR_TYPES) or is_dict_like(obj))


def np_dict_filter(keys, options):
    """
    Filter `options` with given `keys`.

    :param keys: key names of optional keyword arguments
    :param options: optional keyword arguments to filter with `keys`

    >>> filter_options(("aaa", ), dict(aaa=1, bbb=2))
    {'aaa': 1}
    >>> filter_options(("aaa", ), dict(bbb=2))
    {}
    """
    return dict((k, options[k]) for k in keys if k in options)

# vim:sw=4:ts=4:et:

































