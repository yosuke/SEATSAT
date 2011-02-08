#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''grammar file conversion tool for SEAT (Speech Event Action Transfer)

Copyright (C) 2009-2010
    Yosuke Matsusaka and Isao Hara
    Intelligent Systems Research Institute,
    National Institute of Advanced Industrial Science and Technology (AIST),
    Japan
    All rights reserved.
Licensed under the Eclipse Public License -v 1.0 (EPL)
http://www.opensource.org/licenses/eclipse-1.0.txt
'''

import sys
import os
import codecs
import optparse
import locale
from __init__ import __version__
from xml.dom.minidom import parse
import utils
try:
    import gettext
    _ = gettext.translation(domain='seatsat', localedir=os.path.dirname(__file__)+'/../share/locale').ugettext
except:
    _ = lambda s: s

__doc__ = _('Generate W3C-SRGS grammar from the SEAT script file.')

__examples__ = '''
Examples:

- '''+_('Generate SRGS grammar from the SEAT script file.')+'''

  ::
  
  $ seatmltosrgs sample.seatml > sample.grxml
'''

def main():
    encoding = locale.getpreferredencoding()
    sys.stdout = codecs.getwriter(encoding)(sys.stdout, errors = "replace")
    sys.stderr = codecs.getwriter(encoding)(sys.stderr, errors = "replace")

    parser = utils.MyParser(version=__version__, usage="%prog [seatmlfile]",
                            description=__doc__, epilog=__examples__)
    parser.add_option('-v', '--verbose', dest='verbose', action='store_true',
                      default=False,
                      help=_('output verbose information'))
    try:
        opts, args = parser.parse_args()
    except optparse.OptionError, e:
        print >>sys.stderr, 'OptionError:', e
        sys.exit(1)

    if len(args) == 0:
        parser.error("wrong number of arguments")
        sys.exit(1)

    sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

    print '''\
<?xml version="1.0" encoding="UTF-8" ?>
<grammar xmlns="http://www.w3.org/2001/06/grammar"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.w3.org/2001/06/grammar
                             http://www.w3.org/TR/speech-grammar/grammar.xsd"
         xml:lang="jp"
         version="1.0" mode="voice" root="command">

  <lexicon uri="sample-lex.xml"/>

  <rule id="command">
    <one-of>'''
    for f in args[0:]:
        doc = parse(f)
        for s in doc.getElementsByTagName('state'):
            for r in s.getElementsByTagName('rule'):
                for k in r.getElementsByTagName('key'):
                    lab = k.childNodes[0].data
                    print '      <item>%s</item>' % (lab,)
    print '''\
    </one-of>
  </rule>

</grammar>
'''

if __name__=='__main__':
    main()
