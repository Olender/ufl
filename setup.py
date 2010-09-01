#!/usr/bin/env python

from distutils.core import setup
from distutils import sysconfig
from os.path import join as pjoin, split as psplit
import sys
import platform

# Version number
major = 0
minor = 5
maintenance = 4

scripts = [pjoin("scripts", "ufl-analyse"),
           pjoin("scripts", "ufl-convert"),
           pjoin("scripts", "ufl2py"),
           pjoin("scripts", "form2ufl")]

if platform.system() == "Windows" or "bdist_wininst" in sys.argv:
    # In the Windows command prompt we can't execute Python scripts
    # without a .py extension. A solution is to create batch files
    # that runs the different scripts.
    batch_files = []
    for script in scripts:
        batch_file = script + ".bat"
        f = open(batch_file, "w")
        f.write('python "%%~dp0\%s" %%*' % psplit(script)[1])
        f.close()
        batch_files.append(batch_file)
    scripts.extend(batch_files)

setup(name = "UFL",
      version = "%d.%d.%d" % (major, minor, maintenance),
      description = "Unified Form Language",
      author = "Martin Sandve Alnaes, Anders Logg",
      author_email = "ufl@lists.launchpad.net",
      url = "http://www.fenics.org/ufl/",
      scripts = scripts,
      packages = ["ufl", "ufl.algorithms"],
      package_dir = {"ufl": "ufl"},
      data_files = [(pjoin("share", "man", "man1"),
                     [pjoin("doc", "man", "man1", "ufl-analyse.1.gz"),
                      pjoin("doc", "man", "man1", "ufl-convert.1.gz"),
                      pjoin("doc", "man", "man1", "ufl2py.1.gz"),
                      pjoin("doc", "man", "man1", "form2ufl.1.gz")])])
