import time
import multiprocessing as mp

from multiprocessing import Process

def func():
    i = 0
    while True :
      i = i + 1
      print(i)
      time.sleep(1)



if __name__ == '__main__':
    p = Process(target=func)
    p.start()

    i = 0
    while True :
      i = i + 1
      print(i)
      time.sleep(1.5)