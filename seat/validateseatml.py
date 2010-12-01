#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''script validation tool for SEAT (Speech Event Action Transfer)

Copyright (C) 2009-2010
    Yosuke Matsusaka and Isao Hara
    Intelligent Systems Research Institute,
    National Institute of Advanced Industrial Science and Technology (AIST),
    Japan
    All rights reserved.
Licensed under the Eclipse Public License -v 1.0 (EPL)
http://www.opensource.org/licenses/eclipse-1.0.txt
'''

import sys, os, getopt, codecs, locale
from lxml import etree

def usage():
    print "usage: %s [--help] [--gui] [scriptfile]" % (os.path.basename(sys.argv[0]),)
        
def main():
    global guimode
    
    locale.setlocale(locale.LC_CTYPE, "")
    encoding = locale.getlocale()[1]
    if not encoding:
        encoding = "us-ascii"
    sys.stdout = codecs.getwriter(encoding)(sys.stdout, errors = "replace")
    sys.stderr = codecs.getwriter(encoding)(sys.stderr, errors = "replace")

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hg", ["help", "gui"])
    except getopt.GetoptError:
        usage()
        sys.exit()
    guimode = False
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        if o in ("-g", "--gui"):
            import Tkinter, tkFileDialog
            root = Tkinter.Tk()
            root.withdraw()
            args.append(tkFileDialog.askopenfilename(title="select script file"))
            guimode = True
    if len(args) != 1:
        usage()
        sys.exit()
    if hasattr(sys, "frozen"):
        basedir = os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding()))
    else:
        basedir = os.path.dirname(__file__)

    parser = etree.XMLParser(dtd_validation = True)
    xmlschema_doc = etree.parse(os.path.join(basedir, 'seatml.xsd'))
    xmlschema = etree.XMLSchema(xmlschema_doc)
    print "validating script file %s..." % (args[0],)
    try:
        doc2 = etree.parse(args[0])
    except:
        print "xml read error"
        myexit()
    try:
        xmlschema.assert_(doc2)
    except AssertionError, b:
        print "[error] invalid script file."
        print b
        myexit()

    valid = True
    
    for s in doc2.findall('state'):
        for r in s.findall('rule'):
            for k in r.findall('key'):
                if k.text is None:
                    print "[error] line %i: no data in key" % (k.sourceline,)
                    valid = False
            for c in r.findall('command'):
                if c.text is None:
                    print "[error] line %i: no data in command" % (c.sourceline,)
                    valid = False
            for t in r.findall('statetransition'):
                if t.text is None and t.get('func') != "pop":
                    print "[error] line %i: no target in state transition" % (t.sourceline,)
                    valid = False
    
    if (valid == True):
        print "script file is valid."
    myexit()
        
def myexit():
    global guimode
    if guimode == True:
        raw_input("Press Enter to Exit")
    sys.exit()

if __name__ == '__main__':
    main()
