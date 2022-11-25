import time
import multiprocessing as mp

from multiprocessing import Process

def func():
    print("Hello world")

if __name__ == '__main__':
    p = Process(target=func)
    p.start()
    p.join()