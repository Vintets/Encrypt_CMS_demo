#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
from ctypes import windll

stdout_handle = windll.kernel32.GetStdHandle(-11)
SetConsoleTextAttribute = windll.kernel32.SetConsoleTextAttribute


def cprint(cstr):
    clst = cstr.split('^')
    color = 0x0001
    for cstr in clst:
        dglen = re.search('\D', cstr).start()
        if dglen:
            color = int(cstr[:dglen])
        text = cstr[dglen:]
        if text[:1] == '_': text = text[1:]
        SetConsoleTextAttribute(stdout_handle, color | 0x0070) #78
        # print text.replace(u'\u0456', u'i').encode('cp866', 'ignore'),
        sys.stdout.write(text.replace(u'\u0456', u'i').encode('cp866', 'ignore'))
    #sys.stdout.flush()
    print
    SetConsoleTextAttribute(stdout_handle, 0x0001 | 0x0070)

def cprint2(cstr):
    clst = cstr.split('^')
    color = 0x0001
    for cstr in clst:
        dglen = re.search('\D', cstr).start()
        if dglen:
            color = int(cstr[:dglen])
        text = cstr[dglen:]
        if text[:1] == '_': text = text[1:]
        SetConsoleTextAttribute(stdout_handle, color | 0x0070) #78
        # print text.replace(u'\u0456', u'i').encode('cp866', 'ignore'),
        sys.stdout.write(text.replace(u'\u0456', u'i').encode('cp866', 'ignore'))
    sys.stdout.flush()
    SetConsoleTextAttribute(stdout_handle, 0x0001 | 0x0070)

# cprint(u'Обрабатываем файл^5_XXX^13_YYY')
# cprint2(u'Обрабатываем файл^5_XXX^13_YYY')
