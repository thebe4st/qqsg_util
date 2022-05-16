from threading import Thread

def thread_it(func, *args):
    t = Thread(target=func, args=args)
    t.daemon = True
    t.start()