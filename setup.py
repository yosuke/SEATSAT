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
import sys, os
from seatsat.XableRTC import *

version = '1.02'

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
                    "seatsat/SoarRTC.py"
                    ],
        "options": {
            "py2exe": {
                "includes": "xml.etree.ElementTree, lxml._elementpath, OpenRTM_aist, RTC, gzip, seatsat.XableRTC",
                "dll_excludes": ["MSVCP90.dll", "ierutil.dll", "powrprof.dll", "msimg32.dll", "mpr.dll", "urlmon.dll", "dnsapi.dll"],
            }
        }
    }
else:
    extra = {}

setup(name='seatsat',
    version=version,
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
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
        ],
    entry_points="""
    [console_scripts]
    seat = seatsat.SEAT:main
    validateseatml = seatsat.validateseatml:main
    seatmltographviz = seatsat.seatmltographviz:main
    soarrtc = seatsat.SoarRTC:main
    """,
    **extra
    )
