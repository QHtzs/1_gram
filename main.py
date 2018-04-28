# -*- coding:utf-8 -*-

"""
windows
"""
from jieba import dt
from process_queue import SrcLineQueue,LineQueue,FileNameQueue,ToFilterQueue
from util import load_local_words,transfer_list_str,get_filename_in_dir
from mapper import stata_freq
from line_cuts import MyCut
from myfilter import Myfilter
from load_files_lines import LoadFile


from multiprocessing import Process,cpu_count
import sys
import pickle


if __name__ == "__main__":
    #====config ==================
    #download from webs;encoding=utf-8
    stop_word_file = r"stop_words.txt"
    sent_word_file = r"sentiment_score.txt"
    jieba_user_dict_file = ""
    txt_file_dir = r"test"
    #=============================

    # ====== init jieba =====================
    dt.initialize()  #to avoid the object copies initilalize theresevies in each process
    if jieba_user_dict_file:
        dt.load_userdict(jieba_user_dict_file)
    #==========================================

    #=====load dicts =============================================================================
    stop_words = load_local_words(stop_word_file,"UTF-8")
    stop_words = list(stop_words)
    sent_words = load_local_words(sent_word_file,"UTF-8")
    sent_words = list(sent_words) # generator to list

    # if the file occurpied too much mem,user RawArray(wrap of mmap)

    if sys.getsizeof(stop_words) > 1024*1024*1024:
        stop_words = transfer_list_str(stop_words)


    if sys.getsizeof(sent_words) > 1024*1024*1024:
        sent_words = transfer_list_str(sent_words)
    # =========================================================================================

    #====== file ===============================================================
    filenames = get_filename_in_dir(txt_file_dir,"txt")
    for file in filenames:
        FileNameQueue.put_nowait(file)



    SIGNAL_TMS_0 = 2
    SIGNAL_TMS_1 = 2
    if cpu_count() < 4:
        SIGNAL_TMS_0 = 1
        SIGNAL_TMS_1 = 1

    for _ in range(SIGNAL_TMS_0):
        t = LoadFile(FileNameQueue,SrcLineQueue,sent_words,encoding="utf8",force_continue=True)
        t.start()


    sig = int(SIGNAL_TMS_0/SIGNAL_TMS_1) #warnning:to make sure program`s result right,SIGNAL_TMS_0 % SIGNAL_TMS_1 must be 0
    for _ in range(SIGNAL_TMS_1):
        t = MyCut(SrcLineQueue,LineQueue,sig,dt)
        t.start()
        t2 = Process(target=stata_freq,args=(LineQueue,ToFilterQueue,stop_words,))
        t2.start()

    result = Myfilter(ToFilterQueue,SIGNAL_TMS_1)
    print(result)
    res = pickle.dumps(result)
    with open("result1.pkl", 'wb') as f:
        f.write(res)





