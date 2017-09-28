# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from importlib import import_module
from pkgutil import walk_packages
import builtins, operator, inspect, future


import regex, past, ast, re, math,  os, sys, glob, platform
from collections import OrderedDict
from attrdict import AttrDict as dict2


#####################################################################################################
#__path__= '/'
#__version__= "1.0.0"
#__file__= "configmy.py"

'''
Modified in hard  pypi Version number
  1) Update the change log and edit the version number in setup.py   VERSION
  2) Open terminal window and change directory to 
     D:\_devs\Python01\project27\github\configmy
     activate tf_gpu_12    (conda environnment).
     
  3) Write down
     python setup.py sdist bdist_wheel --universal
     twine upload dist/*0.12.5*                

     pip install configmy

'''

#####################################################################################################
import os,sys, re, six
import os.path as op
from subprocess import call
from six.moves import input
from github3 import login


def os_cmd(cmd, system=False):
    if system:
        ret = os.system(cmd)
    else:
        ret = call(cmd.split(' '))
    if ret != 0:
        raise RuntimeError()



def pypi_update_version(findStr,  filePath):
    "replaces all findStr by repStr in file filePath"
    import fileinput
    file1= fileinput.FileInput(filePath, inplace=True, backup='.bak')
    for line in file1:
       if line.find(findStr) == 0 :
         # line= '__version__ = "0.12.2"'
         lversion  =    line.split("=")[-1].replace('"', '').replace("'","").lstrip().split(".")
         lversion[-1]=  str(int(lversion[-1]) + 1)
         version_new= '"' +  '.'.join(lversion) + '"  \n'
         line0=       'VERSION = ' + version_new
         sys.stdout.write(line0)
       else :
         sys.stdout.write(line)
    file1.close()
    print(line0)
    return version_new



# PyPI
def pypi_upload():
    os_cmd('python setup.py sdist --formats=zip upload')



####################################################################################################
version_new= pypi_update_version("VERSION",  "setup.py" )

pypi_upload()










####################################################################################################
# -----------------------------------------------------------------------------
# Messing with version in __init__.py
root = op.realpath(op.join(op.dirname(__file__), '../'))
#_version_pattern = r"__version__ = '([0-9\.]+)((?:\.dev)?)([0-9]+)'"
#_version_replace = r"__version__ = '{}{}{}'"


_version_pattern = r"__version__ = '([0-9\.]+)([0-9\.]+)([0-9]+)'"
_version_replace = r"__version__ = '{}{}{}'"



def _call(cmd, system=False):
    if system:
        ret = os.system(cmd)
    else:
        ret = call(cmd.split(' '))
    if ret != 0:
        raise RuntimeError()




def _path(fn):
    return op.realpath(op.join(root, fn))


def _get_stable_version():
    fn = _path('phy/__init__.py')
    with open(fn, 'r') as f:
        contents = f.read()
    m = re.search(_version_pattern, contents)
    return m.group(1)


def _update_version(dev_n='+1', file0="__init__.py", dev=True):
    fn = _path(file0)
    dev = '.dev' if dev else ''

    def func(m):
        if dev:
            if isinstance(dev_n, six.string_types):
                n = int(m.group(3)) + int(dev_n)
            assert n >= 0
        else:
            n = ''
        if not m.group(2):
            raise ValueError()
        return _version_replace.format(m.group(1), dev, n)

    with open(fn, 'r') as f:
        contents = f.read()

    contents_new = re.sub(_version_pattern, func, contents)

    with open(fn, 'w') as f:
        f.write(contents_new)


def _increment_dev_version():
    _update_version('+1')


def _decrement_dev_version():
    _update_version('-1')


def _set_final_version():
    _update_version(dev=False)


# -----------------------------------------------------------------------------
# Git[hub] tools

def _create_gh_release():
    version = _get_stable_version()
    name = 'Version {}'.format(version)
    path = _path('dist/phy-{}.zip'.format(version))
    assert op.exists(path)

    with open(_path('.github_credentials'), 'r') as f:
        user, pwd = f.read().strip().split(':')
    gh = login(user, pwd)
    phy = gh.repository('kwikteam', 'phy')

    if input("About to create a GitHub release: are you sure?") != 'yes':
        return
    release = phy.create_release('v' + version,
                                 name=name,
                                 # draft=False,
                                 # prerelease=False,
                                 )

    release.upload_asset('application/zip', op.basename(path), path)


def _git_commit(message, push=False):
    assert message
    if input("About to git commit {}: are you sure?") != 'yes':
        return
    _call('git commit -am "{}"'.format(message))
    if push:
        if input("About to git push upstream master: are you sure?") != 'yes':
            return
        _call('git push upstream master')




# -----------------------------------------------------------------------------
# Docker
def _build_docker():
    _call('docker build -t phy-release-test docker/stable')


def _test_docker():
    _call('docker run --rm phy-release-test /sbin/start-stop-daemon --start '
          '--quiet --pidfile /tmp/custom_xvfb_99.pid --make-pidfile '
          '--background --exec /usr/bin/Xvfb -- :99 -screen 0 1400x900x24 '
          '-ac +extension GLX +render && '
          'python -c "import phy; phy.test()"',
          system=True)


# -----------------------------------------------------------------------------
# Release functions
def release_test():
    _increment_dev_version()
    _upload_pypi()
    _build_docker()
    _test_docker()


def release():
    version = _get_stable_version()
    _set_final_version()
    _upload_pypi()
    _git_commit("Release {}.".format(version), push=True)
    _create_gh_release()


if __name__ == '__main__' :
    pass
    # globals()[sys.argv[1]]()   ### Execute the function    python release.py release using global var
    #_update_version(dev_n='+1', file0="setup.py", dev=True)
    #_increment_dev_version()



