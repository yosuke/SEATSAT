#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''SEAT (Speech Event Action Transfer)

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
import getopt
import codecs
import locale
import time
import signal
import re
import traceback
import socket
import threading
import OpenRTM_aist
import RTC
from lxml import etree
from BeautifulSoup import BeautifulSoup

class SocketAdaptor(threading.Thread):
    def __init__(self, seat, name, host, port):
        threading.Thread.__init__(self)
        self.seat = seat
        self.name = name
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.mainloop = True
        self.start()

    def run(self):
        while self.mainloop:
            if self.connected == False:
                try:
                    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.socket.connect((self.host, self.port))
                    self.socket.settimeout(1)
                    self.connected = True
                except socket.error:
                    print "reconnect error"
                    time.sleep(1)
                except:
                    print traceback.format_exc()
            if self.connected == True:
                try:
                    data = self.socket.recv(1024)
                    if len(data) != 0:
                        self.seat.processResult(self.name, data)
                except socket.timeout:
                    pass
                except socket.error:
                    print traceback.format_exc()
                    self.socket.close()
                    self.connected = False
                except:
                    print traceback.format_exc()

    def terminate(self):
        self.mainloop = False
        if self.connected == True:
            self.socket.close()
            self.connected = False
        
    def send(self, name, msg):
        if self.connected == False:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.host, self.port))
                self.connected = True
            except socket.error:
                print "cannot connect"
        if self.connected == True:
            try:
                self.socket.sendall(msg)
            except socket.error:
                print traceback.format_exc()
                self.socket.close()
                self.connected = False

seat_spec = ["implementation_id", "SEAT",
             "type_name",         "SEAT",
             "description",       "Speech Event Action Transfer",
             "version",           "1.0.0",
             "vendor",            "Yosuke Matsusaka and Isao Hara, AIST",
             "category",          "Speech",
             "activity_type",     "DataFlowComponent",
             "max_instance",      "1",
             "language",          "Python",
             "lang_type",         "script",
             "conf.default.scriptfile", "none",
             "exec_cxt.periodic.rate", "100.0",
             ""]

class DataListener(OpenRTM_aist.ConnectorDataListenerT):
    def __init__(self, name, type, obj):
        self._name = name
        self._type = type
        self._obj = obj
    
    def __call__(self, info, cdrdata):
        data = OpenRTM_aist.ConnectorDataListenerT.__call__(self, info, cdrdata, self._type(RTC.Time(0,0),None))
        self._obj.onData(self._name, data)


class SEAT(OpenRTM_aist.DataFlowComponentBase):
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
        
        if hasattr(sys, "frozen"):
            self._basedir = os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding()))
        else:
            self._basedir = os.path.dirname(__file__)
        xmlschema_doc = etree.parse(os.path.join(self._basedir, 'seatml.xsd'))
        self._xmlschema = etree.XMLSchema(xmlschema_doc)

        self.states = []
        self.currentstate = "start"
        self.keys = {}
        self.regkeys = {}
        self.adaptors = {}
        self.adaptortype = {}
        self.statestack = []
        self._data = {}
        self._port = {}
        self._scriptfile = ["none"]
        print "component created"

    def onInitialize(self):
        self.bindParameter("scriptfile", self._scriptfile, "none", self.scriptfileTrans)
        return RTC.RTC_OK

    def onFinalize(self):
        try:
            for a in self.adaptors.itervalues():
                if isinstance(a, SocketAdaptor):
                    a.terminate()
                    a.join()
        except:
            print traceback.format_exc()
        return RTC.RTC_OK

    def scriptfileTrans(self, _type, _str): 
        print "scriptfile = " + _str
        if _str != "none":
            try:
                self.loadSEATML(_str.split(','))
            except:
                print traceback.format_exc()
        return OpenRTM_aist.stringTo(_type, _str)

    def createInPort(self, name, type=RTC.TimedString):
        print "create inport: " + name
        self._data[name] = type(RTC.Time(0,0), None)
        self._port[name] = OpenRTM_aist.InPort(name, self._data[name])
        self._port[name].addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_WRITE,
                                                  DataListener(name, type, self))
        self.registerInPort(name, self._port[name])

    def createOutPort(self, name, type=RTC.TimedString):
        print "create outport: " + name
        self._data[name] = type(RTC.Time(0,0), None)
        self._port[name] = OpenRTM_aist.OutPort(name, self._data[name], OpenRTM_aist.RingBuffer(8))
        self.registerOutPort(name, self._port[name])

    def onData(self, name, data):
        try:
            if isinstance(data, RTC.TimedString):
                data.data = data.data.decode('utf-8')
            self.processResult(name, data.data)
        except:
            print traceback.format_exc()

    def onExecute(self, ec_id):
        time.sleep(1)
        return RTC.RTC_OK

    def send(self, name, data):
        print "sending command %s (%s)" % (data, name)
        dtype = self.adaptortype[name][1]
        if dtype == str:
            ndata = dtype(data.encode('utf-8'))
        elif self.adaptortype[name][2]:
            ndata = []
            for d in data.split(","):
                ndata.append(dtype(d))
        else:
            ndata = dtype(data)
        self._data[name].data = ndata
        self._port[name].write()

    def processResult(self, host, s):
        try:
            s = unicode(s)
        except UnicodeDecodeError:
            s = str(s).encode('string_escape')
            s = unicode(s)
        print "got input %s (%s)" % (s, host)
        cmds = None
        if s.count('<?xml') > 0:
            doc = BeautifulSoup(s)
            for s in doc.findAll('data'):
                words = []
                for w in s.findAll('word'):
                    word = w['text']
                    words.append(word)
                cmds = self.lookupwithdefault(self.currentstate, host, ' '.join(words))
                if not cmds:
                    cmds = self.lookupwithdefault(self.currentstate, host, ''.join(words))
                if cmds:
                    break
        else:
            cmds = self.lookupwithdefault(self.currentstate, host, s)
        if not cmds:
            print "no command found"
            return False
        for c in cmds:
            self.activateCommand(c)
        return True

    def lookupwithdefault(self, state, host, s):
        print 'looking up... %s' % (s,)
        cmds = self.lookupcommand(state, host, s)
        if not cmds:
            cmds = self.lookupcommand(state, 'default', s)
        if not cmds:
            cmds = self.lookupcommand('all', host, s)
        if not cmds:
            cmds = self.lookupcommand('all', 'default', s)
        return cmds

    def lookupcommand(self, state, host, s):
        cmds = []
        regkeys = []
        try:
            cmds = self.keys[state+":"+host+":"+s]
        except KeyError:
            try:
                regkeys = self.regkeys[state+":"+host]
            except KeyError:
                return None
            for r in regkeys:
                if r[0].match(s):
                    cmds = r[1]
                    break
            return None
        return cmds
        

    def activateCommand(self, c):
        if c[0] == 'c':
            host = c[1]
            data = c[2]
            try:
                ad = self.adaptors[host]
                ad.send(host, data)
            except KeyError:
                print "no such adaptor"
        elif c[0] == 't':
            func = c[1]
            data = c[2]
            if (func == "push"):
                self.statestack.append(self.currentstate)
                self.currentstate = data
            elif (func == "pop"):
                if self.statestack.__len__() == 0:
                    print "state buffer is empty"
                    return
                self.currentstate = self.statestack.pop()
            else:
                print "state transition from "+self.currentstate+" to "+data
                self.currentstate = data

    def getDataType(self, s):
        if len(s) == 0:
            return (RTC.TimedString, 0)
        seq = False
        if s[-3:] == "Seq":
            seq = True
        dtype = str
        if s.count("WString"):
            dtype = unicode
        elif s.count("Float"):
            dtype = float
        elif s.count("Double"):
            dtype = float
        elif s.count("Short"):
            dtype = int
        elif s.count("Long"):
            dtype = int
        elif s.count("Octet"):
            dtype = int
        elif s.count("Char"):
            dtype = int
        elif s.count("Boolean"):
            dtype = int
        return (eval("RTC.%s" % s), dtype, seq)

    def loadSEATML(self, files):
        for f in files:
            f = f.replace("\\", "\\\\")
            #print "load script file: " + f
            try:
                doc = etree.parse(f)
            except etree.XMLSyntaxError, e:
                print "[error] invalid xml syntax"
                print e
                sys.exit()
            except IOError, e:
                print "[error] IO error: unable to open file " + f
                print e
                sys.exit()
            try:
                self._xmlschema.assert_(doc)
            except AssertionError, b:
                print "[error] invalid script file: " + f
                print b
                continue
            for g in doc.findall('general'):
                for a in g.findall('agent'):
                    name = str(a.get('name'))
                    type = a.get('type')
                    if type == 'rtcout':
                        self.adaptortype[name] = self.getDataType(a.get('datatype'))
                        self.createOutPort(name, self.adaptortype[name][0])
                        self.adaptors[name] = self
                    elif type == 'rtcin':
                        self.adaptortype[name] = self.getDataType(a.get('datatype'))
                        self.createInPort(name, self.adaptortype[name][0])
                        self.adaptors[name] = self
                    else:
                        host = a.get('host')
                        port = int(a.get('port'))
                        self.adaptors[name] = SocketAdaptor(self, name, host, port)
            for s in doc.findall('state'):
                name = s.get('name')
                for r in s.findall('rule'):
                    words = []
                    commands = []
                    for c in r.findall('command'): # get commands
                        host = c.get('host')
                        data = c.text
                        commands.append(['c', host, data])
                    for c in r.findall('statetransition'): # get statetransition (as command)
                        func = c.get('func')
                        data = c.text
                        commands.append(['t', func, data])
                    for k in r.findall('key'): # get keys
                        source = k.get('source')
                        word = self.decompString([k.text])
                        if source is None:
                            words.extend(word)
                        else:
                            for w in word:
                                print "register "+name+":"+source+":"+w
                                self.keys[name+":"+source+":"+w] = commands # register commands to key table
                    for k in r.findall('regkey'): # get keys
                        try:
                            regkeys = self.regkeys[name+":default"]
                        except KeyError:
                            regkeys = []
                        regkeys.append([re.compile(k.text), commands])
                        self.regkeys[name+":default"] = regkeys
                    for w in words:
                        print "register " + name + ":default:" + w
                        self.keys[name+":default:"+w] = commands # register commands to key table
                self.states.extend([name])
        if len(self.states) == 0:
            print "[error] no available state"
            exit()
        if self.states.count("start") > 0:
            self.currentstate = "start"
        else:
            self.currentstate = self.states[0]
        print "current state " + self.currentstate
        print "Started successfully"

    def decompString(self, strs):
        ret = []
        nstrs = strs
        while nstrs.__len__() > 0:
            nstrs2 = []
            for str in nstrs:
                if str.count('(') > 0 or str.count('[') > 0:
                    nstrs2.extend(self.decompStringSub(str))
                else:
                    ret.extend([str])
            nstrs = nstrs2
        return ret

    def decompStringSub(self, str):
        ret = []
        bc = str.count('(')
        kc = str.count('[')
        if bc > 0:
            i = str.index('(')
            prestr = str[:i]
            substrs = []
            substr = ''
            level = 0
            i += 1
            while i < str.__len__():
                if str[i] == '(':
                    level += 1
                    substr += str[i]
                elif str[i] == ')':
                    if level == 0:
                        substrs.extend([substr])
                        break
                    else:
                        substr += str[i]
                    level -= 1
                elif str[i] == '|':
                    if level == 0:
                        substrs.extend([substr])
                        substr = ''
                    else:
                        substr += str[i]
                else:
                    substr += str[i]
                i += 1
            poststr = str[i+1:]
            for s in substrs:
                ret.extend([prestr+s+poststr])
        elif kc > 0:
            i = str.index('[')
            prestr = str[:i]
            substr = ''
            level = 0
            i += 1
            while i < str.__len__():
                if str[i] == '[':
                    level += 1
                elif str[i] == ']':
                    if level == 0:
                        break
                    level -= 1
                substr += str[i]
                i += 1
            poststr = str[i+1:]
            ret.extend([prestr+poststr])
            ret.extend([prestr+substr+poststr])
        else:
            ret.extend([str])
        return ret

class SEATManager:
    def __init__(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "adlf:o:p:hg", ["help", "gui"])
        except getopt.GetoptError:
            usage()
            sys.exit()
        managerargs = [sys.argv[0]]
        for o, a in opts:
            if o in ("-a", "-d", "-l"):
                managerargs.append(o)
            if o in ("-f", "-o", "-p"):
                managerargs.append(o, a)
            if o in ("-h", "--help"):
                usage()
                sys.exit()
            if o in ("-g", "--gui"):
                import Tkinter, tkFileDialog
                root = Tkinter.Tk()
                root.withdraw()
                sel = tkFileDialog.askopenfilenames(title="select script files")
                if isinstance(sel, unicode):
                    sel = root.tk.splitlist(sel)
                args.extend(sel)
        if len(args) <= 0:
            usage()
            sys.exit()
        self._scriptfiles = args
        self.comp = None
        self.manager = OpenRTM_aist.Manager.init(managerargs)
        self.manager.setModuleInitProc(self.moduleInit)
        self.manager.activateManager()

    def start(self):
        self.manager.runManager(False)

    def moduleInit(self, manager):
        profile=OpenRTM_aist.Properties(defaults_str=seat_spec)
        manager.registerFactory(profile, SEAT, OpenRTM_aist.Delete)
        self.comp = manager.createComponent("SEAT?exec_cxt.periodic.rate=1")
        self.comp.loadSEATML(self._scriptfiles)

def usage():
    print "usage: %s [-f rtc.conf] [--help] [--gui] [scriptfile]" % (os.path.basename(sys.argv[0]),)

def main():
    locale.setlocale(locale.LC_CTYPE, "")
    encoding = locale.getlocale()[1]
    if not encoding:
        encoding = "us-ascii"
    sys.stdout = codecs.getwriter(encoding)(sys.stdout, errors = "replace")
    sys.stderr = codecs.getwriter(encoding)(sys.stderr, errors = "replace")

    seat = SEATManager()
    seat.start()

if __name__=='__main__':
    main()

