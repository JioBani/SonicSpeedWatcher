import time

class StopWatch : 
    
    def __init__(self) :
        self.__current  = 0
        self.__isRun = False
        self.__startTime = 0
        
    def start(self):
        self.__isRun = True
        self.__startTime = time.time()
    
    def stop(self):
        self.__isRun = False
        
    def reset(self):
        self.__current = 0
        self.__isRun = False
    
    def reStart(self):
        self.__isRun = True
        
    
    def getTime(self):
        
        if(self.__isRun):
            self.__current = time.time() -  self.__startTime
            
        return self.__current
    
    def isRun(self):
        return self.__isRun