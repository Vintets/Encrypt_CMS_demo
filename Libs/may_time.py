#!/usr/bin/env python
# -*- coding: utf-8 -*-

def clock_hms(time_s, zero=True, ms=True):
    '''
    Convert time sec to str H:M:S
    param zero -->  00:00:00 / 0:0:0
    param ms   -->  00:00:00.000/ 00:00:00
    '''

    h = int(time_s/3600)
    m = int((time_s - h*3600)/60)
    s = round(time_s - h*3600 - m*60, 3)
    if zero:
        if ms: out = u'%02d:%02d:%06.3f' % (h, m, s)
        else:  out = u'%02d:%02d:%02d' % (h, m, s)
    else:
        if ms: out = u'%d:%d:%.3f' % (h, m, s)
        else:  out = u'%d:%d:%d' % (h, m, s)
    # print u'Время: %s' % (out)
    return out
