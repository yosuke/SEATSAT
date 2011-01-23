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

import sys, os, codecs
from xml.dom.minidom import parse

def main():
    if len(sys.argv) < 2:
        print "usage: %s [seatml]" % sys.argv[0]
        quit()

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
    for f in sys.argv[1:]:
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
