#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''visualization tool for SEAT (Speech Event Action Transfer)

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

if len(sys.argv) < 2:
    print "usage: %s [seatml]" % sys.argv[0]
    quit()

sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

print 'digraph seatml {'
print 'graph [rankdir=LR];'

doc = parse(sys.argv[1])
states = map(lambda x:x.getAttribute('name'), doc.getElementsByTagName('state'))
states.extend(map(lambda x:x.childNodes[0].data, doc.getElementsByTagName('statetransition')))
print 'node [shape = doublecircle]; %s;' % ' '.join(states)
print 'node [shape = circle];'
#print 'edge [fontname = "osaka"];'

for f in sys.argv[1:]:
    doc = parse(f)
    for s in doc.getElementsByTagName('state'):
        for r in s.getElementsByTagName('rule'):
            lab = '[label = "'
            #lab = lab + ",".join(map(lambda x: x.childNodes[0].data, r.getElementsByTagName('key')))
            source = r.getElementsByTagName('key').item(0).getAttribute('source')
            if source:
                lab = lab + source + "="
            lab = lab + r.getElementsByTagName('key').item(0).childNodes[0].data
            lab = lab + '"]'
            t = r.getElementsByTagName('statetransition')
            if len(t) > 0:
                print "%s -> %s %s;" % (s.getAttribute('name'), t.item(0).childNodes[0].data, lab)
            else:
                print "%s -> %s %s;" % (s.getAttribute('name'), s.getAttribute('name'), lab)
print '}'
