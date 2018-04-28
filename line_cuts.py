# -*- coding:utf-8 -*-


from multiprocessing import Process

"""

"""

class MyCut(Process):
    def __init__(self,srcline_queue,line_queue,signal_tms,_jieba):
        """
        :param srcline_queue:
        :param line_queue:
        :param signal_tms:
        :param _jieba: jieba module Tokenzener()
        """
        super(MyCut,self).__init__()
        self.srcLineQueue = srcline_queue
        self.lineQueue = line_queue
        self.jieba = _jieba
        self.tms = signal_tms

    def run(self):
        while self.tms>0:
            line,words = self.srcLineQueue.get()
            if isinstance(line,int):
                self.tms -= 1
                continue
            line_list = list(self.jieba.cut(line))#genertor to list
            self.lineQueue.put((line_list,words))
        self.lineQueue.put((0,0)) # emit signal


