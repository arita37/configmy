from __future__ import absolute_import
from setuptools import setup, Command

import glob, os, subprocess, sys
import os.path

global VERSION, PACKAGE

VERSION = "0.14.11"  
PACKAGE = "configmy"


'''
  UPLOAD to Pypi 
  1) Update the change log and edit the version number in setup.py   VERSION
  
  2) Open terminal window and change directory to 
     D:\_devs\Python01\project27\github\configmy
     activate tf_gpu_12    (conda environnment).
     
  3) Write down
      python setup.py sdist --formats=zip upload
     
     
     python setup.py sdist bdist_wheel --universal
     twine upload dist/*0.13.9*                

     pip install configmy==0.13.9

http://5minutes.youkidea.com/howto-deploy-python-package-on-pypi-with-github-and-travis.html

https://blog.jetbrains.com/pycharm/2017/05/how-to-publish-your-package-on-pypi/

'''


##########################################################################################
sys.path.insert(0, os.path.dirname(__file__))  # load  from this dir.


# For daily snapshot versioning mode:
if os.environ.get("_SNAPSHOT_BUILD", None) is not None:
    import datetime
    VERSION = VERSION + datetime.datetime.now().strftime(".%Y%m%d")


_LONG_DESC = """
configmy [#]_ is a `MIT licensed <http://opensource.org/licenses/MIT>`_

python library to access config in  a very flexible way

- Home:  https://github.com/arita37/configmy
- PyPI:  https://pypi.python.org/pypi/configmy


#Test
Sometimes, you have hard coded paths, dependant on system environnment (linux, windows).
Doing  if os.system ="linux" :  is boring.

Configmy load dynamically env. with a single lineof code (!),
Your code can work anywhere, you just need to change the master config file
and the paths inside.

Example :
import configmy
configmy.get("configmy/ztest/test_config.py", output= ["_CFG", "DIRCWD",])


### Set the master file in ENVIRONNEMNT variable
configmy.set( "configmy/ztest/test_config.py") 
CFG, DIRCWD= configmy.get(output= ["_CFG", "DIRCWD",], method)

CFG: a dict containing all the needed paths
DIRCWD:  Main path


In CFG your get the configuration based on os_usernamr tag
( win_Myuser0
  lin_Myuser1
  mac_Myuser2



"""

def list_filepaths(tdir):
    return [f for f in glob.glob(os.path.join(tdir, '*')) if os.path.isfile(f)]




class SrpmCommand(Command):
    user_options = []
    build_stage = "s"

    curdir = os.path.abspath(os.curdir)
    # rpmspec = os.path.join(curdir, "pkg/package.spec")
    # gen_readme = os.path.join(curdir, "pkg/gen-readme.sh")

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.pre_sdist()
        self.run_command('sdist')
        self.build_rpm()

    def pre_sdist(self):
        c = open(self.rpmspec + ".in").read()
        open(self.rpmspec, "w").write(c.replace("@VERSION@", VERSION))
        subprocess.check_call(self.gen_readme, shell=True)

    def build_rpm(self):
        rpmbuild = os.path.join(self.curdir, "pkg/rpmbuild-wrapper.sh")
        workdir = os.path.join(self.curdir, "dist")

        cmd_s = "%s -w %s -s %s %s" % (rpmbuild, workdir, self.build_stage,
                                       self.rpmspec)
        subprocess.check_call(cmd_s, shell=True)


class RpmCommand(SrpmCommand):
    build_stage = "b"


_CLASSIFIERS = ["Development Status :: 4 - Beta",
                "Intended Audience :: Developers",
                "Programming Language :: Python",
                "Programming Language :: Python :: 2",
                "Programming Language :: Python :: 3",
                "Programming Language :: Python :: 2.6",
                "Programming Language :: Python :: 2.7",
                "Programming Language :: Python :: 3.3",
                "Programming Language :: Python :: 3.4",
                "Programming Language :: Python :: 3.5",
                "Programming Language :: Python :: 3.6",
                "Environment :: Console",
                "Operating System :: OS Independent",
                "Topic :: Software Development :: Libraries :: Python Modules",
                "Topic :: Text Processing :: Markup",
                "Topic :: Utilities",
                "License :: OSI Approved :: MIT License"]


setup(name=PACKAGE,
      version=VERSION,
      description=("Library provides very flexible config file loading, in 1 line"),
      long_description=_LONG_DESC,
      author="Kevin Noel",
      author_email="",
      license="MIT",
      url="https://github.com/arita37/configmy",
      classifiers=_CLASSIFIERS,
      packages=["configmy"],
      include_package_data=True,
      cmdclass={
          #"srpm": #SrpmCommand,
          #"rpm":  RpmCommand,
      },
      entry_points= "",     # open(os.path.join(os.curdir, "pkg/entry_points.txt")).read(),
      data_files=""   )     # data_files)



# vim:sw=4:ts=4:et:








