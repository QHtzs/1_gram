
# -*- coding:utf-8 -*-

from util import scaner_word

def stata_freq(line_queue,filter_queue,stop_words):
    if isinstance(stop_words,(list,tuple)):
        stop_words_set = frozenset(stop_words)
    else:
        stop_words_set = 0

    while True:
        line_list,word_list = line_queue.get()
        if isinstance(line_list,int):
            print("mapper finish...")
            filter_queue.put(0)
            break
        if isinstance(stop_words_set,int):
            for word in scaner_word(stop_words):
                if word in line_list:
                    line_list.remove(word)
        else:
            line_list = list(set(line_list) - stop_words_set)

        for word in word_list:
            try:
                ind = line_list.index(word)
            except:
                continue
            if len(line_list)<=1:
                continue
            if ind == len(line_list)-1:
                filter_queue.put({word:{"h":line_list[ind-1],"t":""}}) # h词前词，t词后词
            elif ind == 0:
                filter_queue.put({word:{"h":"","t":line_list[ind+1]}})
            else:
                filter_queue.put({word:{"h":line_list[ind-1],"t":line_list[ind+1]}})

