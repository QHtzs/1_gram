# -*- coding:utf-8 -*-


from multiprocessing import Process
from util import scaner_word

class LoadFile(Process):
    def __init__(self,t_q_filename,p_q_srcline,word_dict,encoding="utf8",force_continue=False):
        super(LoadFile,self).__init__()
        self.fileNameQueue = t_q_filename
        self.scrLineQueue = p_q_srcline
        self._dict = word_dict
        self._encoding = encoding
        self._force = force_continue



    def run(self):
        while True:
            #===========io =====================
            fileName = self.fileNameQueue.get()
            try:
                with open(fileName,mode="r",encoding=self._encoding) as f:
                    lines = f.readlines() #readlines fast and need less mem
            except Exception as e:
                try:
                    e = str(e).encode("unicode_escape").decode("utf-8")
                except:
                    e = "can decode file by %s"%self._encoding
                if not self._force:
                    print("failed to readfile ,thread %s exit. excptions:%s"%(self.name,e))
                    self.scrLineQueue.put((0,0))
                    break
                else:
                    print("failed to readfile ,thread %s continue. excptions:%s" %(self.name,e))
                    continue
            #=========== end =======================

            #====== cpu  this part takes more time,running in another process seems better=====================
            for line in lines:
                words = []
                if isinstance(self._dict,(list,tuple)):
                    for word in self._dict:
                        if word in line:
                            words.append(word)
                else:
                    for word in scaner_word(self._dict):
                        if word in line:
                            words.append(word)
                if words:
                    self.scrLineQueue.put((line,words))
            #======== end =========================================================================

            if self.fileNameQueue.empty():
                self.scrLineQueue.put((0,0))
                # (0,0) as signal
                print("process successed finished")
                break








