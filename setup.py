#!/usr/bin/env python

'''setup script for SEAT and SAT

Copyright (C) 2009-2010
    Yosuke Matsusaka and Isao Hara
    Intelligent Systems Research Institute,
    National Institute of Advanced Industrial Science and Technology (AIST),
    Japan
    All rights reserved.
Licensed under the Eclipse Public License -v 1.0 (EPL)
http://www.opensource.org/licenses/eclipse-1.0.txt
'''

from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext
import sys, os
from seatsat.__init__ import __version__

cmd_classes = {}
try:
    from DistUtilsExtra.command import *
    cmd_classes.update({"build": build_extra.build_extra,
                        "build_i18n" :  build_i18n.build_i18n})
except ImportError:
    pass

try:
    import py2exe
except ImportError:
    pass

if sys.platform == "win32":
    # py2exe options
    extra = {
        "console": [
                    "seatsat/SEAT.py",
                    "seatsat/validateseatml.py",
                    "seatsat/seatmltographviz.py",
                    "seatsat/seatmltosrgs.py",
                    "seatsat/seateditor.py",
                    "seatsat/SoarRTC.py"
                    ],
        "options": {
            "py2exe": {
                "includes": "xml.etree.ElementTree, lxml._elementpath, BeautifulSoup, OpenRTM_aist, RTC, gzip, cairo, pango, pangocairo, atk, gobject, gio, glib, gtk, gtksourceview2",
                "dll_excludes": ["MSVCP90.dll", "ierutil.dll", "powrprof.dll", "msimg32.dll", "mpr.dll", "urlmon.dll", "dnsapi.dll"],
            }
        }
    }
else:
    extra = {}

setup(name='seatsat',
      cmdclass=cmd_classes,
      version=__version__,
      description="Simple dialogue manager component for OpenRTM (part of OpenHRI softwares)",
      long_description="""Simple dialogue manager component for OpenRTM (part of OpenHRI softwares).""",
      classifiers=[],
      keywords='',
      author='Yosuke Matsusaka',
      author_email='yosuke.matsusaka@aist.go.jp',
      url='http://openhri.net/',
      license='EPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      package_data={'seatsat': ['*.xsd',]},
      zip_safe=False,
      install_requires=[
        # -*- Extra requirements: -*-
        ],
      entry_points="""
      [console_scripts]
      seat = seatsat.SEAT:main
      validateseatml = seatsat.validateseatml:main
      seateditor = seatsat.seateditor:main
      seatmltographviz = seatsat.seatmltographviz:main
      seatmltosrgs = seatsat.seatmltosrgs:main
      soarrtc = seatsat.SoarRTC:main
      """,
      **extra
      )
