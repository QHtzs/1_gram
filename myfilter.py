# -*- coding:utf-8 -*-

import re

def combine(list_,dic1): # alter data without copy
    h = dic1.get("h")
    t = dic1.get("t")
    if re.findall('^\d+$|^\s+$',h):
        h = ""
    if re.findall('^\d+$|^\s+$',t):
        t = ""
    if h:
        list_[0].update({h:1+list_[0].get(h,0)})
    if t:
        list_[1].update({t:1+list_[1].get(t, 0)})


def Myfilter(dict_queue,signal_tms):
    result = {}
    while signal_tms:
        info = dict_queue.get()
        if isinstance(info,int):
            signal_tms -= 1
            continue
        for k,v in info.items():
            list_ = result.get(k,[{},{}])
            combine(list_,v)
            result[k] = list_
    return result