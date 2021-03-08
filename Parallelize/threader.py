import threading

class Threader(object):
    def __init__(self, thread_type=threading.Thread):
        self.thread = thread_type

    def NewTread(self, target, args=()):
        t = self.thread(target=target, args=args)
        t.daemon = True
        t.start()
        return t
    
    def Join(self, thread):
        thread.join()