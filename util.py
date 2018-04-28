# -*- coding:utf-8 -*-

from multiprocessing.sharedctypes import RawArray
import os
import re

def load_local_words(file,encoding="utf8"):
    with open(file,mode="r",encoding=encoding) as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        word = line.split()
        word = word[0] if word else ""
        if word:
            yield word

#seriesize
def transfer_list_str(word_map):
    list0 = []
    for word in word_map:
        if len(word) == 0:
            continue
        elif len(word) < 10:
            length = "%i"%len(word)
            list0.append(length)
        else:
            length = "%i" % len(word)
            num_len ="%i"%len(length)
            list0.append("0")
            list0.append(num_len)
            list0.extend(length)
        list0.extend(word)
    return RawArray("u",list0) #RawArray no lock

#deseriesize
def scaner_word(shared_rawarray):
    length = len(shared_rawarray)
    step = 0
    while step<length-1:
        ind = int(shared_rawarray[step])
        if ind > 0:
            step += 1
            word = shared_rawarray[step:step+ind]
            step += ind
            yield word
        else:
            step += 1
            _length = int(shared_rawarray[step])
            step += 1
            ind = int(shared_rawarray[step:step+_length])
            step += _length
            word = shared_rawarray[step:step+ind]
            step += ind
            yield word

#deseriesize
def scaner_word_d(shared_rawarray):
    case = 1
    ind = 0
    word = ""
    buff = 0
    for w_char in shared_rawarray:
        if case is 1:
            if buff is 0:
                ind = 10*ind + int(w_char)
                if ind == 0:
                    case = 2 #next word
                else:
                    case = 0
            else:
                ind = 10*ind + int(w_char)
                buff -= 1
        elif case is 2:
            buff = int(w_char) - 1
            case = 1
        elif case is 0:
            ind -= 1
            if ind == 0:
                case = 1
                word += w_char
                yield word
                word = ""
            else:
                word += w_char


def get_filename_in_dir(path,accept_type="txt|html"):
    accept_types = accept_type.split("|")
    accept_types = [".%s$"%accept for accept in accept_types]
    accept_types = "|".join(accept_types)
    reg = re.compile(accept_types,flags=re.I)
    files = os.listdir(path)
    files = [file for file in files if reg.findall(file)]
    files = [os.path.join(path,file) for file in files]
    return files





