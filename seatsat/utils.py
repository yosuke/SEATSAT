#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Utility functions

Copyright (C) 2010
    Yosuke Matsusaka
    Intelligent Systems Research Institute,
    National Institute of Advanced Industrial Science and Technology (AIST),
    Japan
    All rights reserved.
Licensed under the Eclipse Public License -v 1.0 (EPL)
http://www.opensource.org/licenses/eclipse-1.0.txt
'''

import sys
import os
import platform

def askopenfilename(title=''):
    if platform.system() == 'Windows':
        import win32ui
        import win32con 
        openFlags = win32con.OFN_FILEMUSTEXIST|win32con.OFN_EXPLORER
        fspec = "*.*||"
        dlg = win32ui.CreateFileDialog(1, None, None, openFlags, fspec) 
        if dlg.DoModal() == win32con.IDOK: 
            return dlg.GetPathName()
    else:
        import Tkinter
        import tkFileDialog
        rt = Tkinter.Tk()
        rt.withdraw()
        return tkFileDialog.askopenfilename(title=title)
    return None

def askopenfilenames(title=''):
    if platform.system() == 'Windows':
        import win32ui
        import win32con 
        openFlags = win32con.OFN_FILEMUSTEXIST|win32con.OFN_EXPLORER|win32con.OFN_ALLOWMULTISELECT
        fspec = "all|*.*||"
        dlg = win32ui.CreateFileDialog(1, None, None, openFlags, fspec) 
        if dlg.DoModal() == win32con.IDOK: 
            return dlg.GetPathNames()
    else:
        import Tkinter
        import tkFileDialog
        rt = Tkinter.Tk()
        rt.withdraw()
        sel = tkFileDialog.askopenfilenames(title=title)
        if isinstance(sel, unicode):
            sel = root.tk.splitlist(sel)
        return sel
    return None
