=======
SEATSAT
=======

Dialog manager components for OpenRTM (part of OpenHRI softwares)

Requirements
------------

SEATSAT requires following libraries:

lxml
  http://codespeak.net/lxml/

BeautifulSoup
  http://www.crummy.com/software/BeautifulSoup/

Soar
  http://sitemaker.umich.edu/soar/home

If you are using ubuntu, required libraries will be installed by entering
following commands:

 ::

 $ sudo apt-add-repository ppa:openhri/ppa
 $ sudo apt-get update
 $ sudo apt-get install python-lxml python-beautifulsoup soar-core python-soar

Installation
------------

There are several methods of installation available:

1. Install ubuntu package (recommended):

 a. Register OpenHRI private package archive:

  ::
   
  $ sudo apt-add-repository ppa:openhri/ppa

 b. Install SEATSAT package:

  ::
  
  $ sudo apt-get update
  $ sudo apt-get install seatsat

2. Clone the source from the repository and install:

 a. Clone from the repository:

  ::
  
  $ git clone git://github.com/yosuke/SEATSAT.git SEATSAT

 b. Run setup.py:

  ::
  
  $ cd SEATSAT
  $ sudo python setup.py install

Components
----------

SEAT
  Simple dialog manager component.

SoarRTC
  Soar general artificial intelligence component.

see https://github.com/yosuke/SEATSAT/tree/master/doc for description of each components.

Utility scripts
---------------

validateseatml
  Validate format of SEAT script file.

seatmltosrgs
  Generate W3C-SRGS grammar from SEAT script file.

seatmltographviz
  Draw graph from SEAT script file.

Examples:

- Validate format of the SEAT script file.

  ::
  
  $ validateseatml sample.seatml

- Generate SRGS grammar from the SEAT script file.

  ::
  
  $ seatmltosrgs sample.seatml > sample.grxml
 
- Draw graph of the SEAT script file.

  ::
  
  $ seatmltographviz sample.seatml | dot -Txlib


Changelog
---------

SEATSAT-1.0

- First version.
