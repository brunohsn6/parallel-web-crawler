from threading import Thread, Lock
from job import Job
import time
from enum import Enum

class State(Enum):
    WAITING = 0
    RUNNING = 1
    DONE = 2

class MyThreadPool:
    def __init__(self, maxWorkers):
        self.state = State.WAITING
        self.mutex = Lock()
        self.counter = 0
        self.pool = set([])
        self.maxWorkers = maxWorkers
        self.currentQtdWorkers = 0
        self.currentWorkers = set([])
        self.thread_safe = True
    
    def run(self):
        self.state = State.RUNNING
        while(self.state is not State.DONE):
            self.startNewJob()
            self.verifyThreadsState()
        

    def startNewJob(self):
        if(self.currentQtdWorkers < self.maxWorkers):
            if self.pool:
                with self.mutex:
                    job = self.pool.pop()
                
                try:
                    print("starting thread")
                    th = Thread(target=job.function, args=(job.args,))
                    th.start()
                    
                    with self.mutex:
                        self.currentWorkers.add(th)
                        self.currentQtdWorkers+=1
                        
                except Exception as e:
                    print("a execução da thread falhou!")
                    print(th)
                    print(e)
                
                    
    
    def submit(self, func, args):
        newExec = Job(func, args)
        with self.mutex:
            self.pool.add(newExec)
            print("submitted")
            self.counter +=1
        
        
    def verifyThreadsState(self):
        with self.mutex:
            toRemove = set([])
            for th in self.currentWorkers:
                if not th.isAlive():
                    #just to make sure that the thread that isn't running anymore is killed
                    toRemove.add(th)
            for td in toRemove:
                    self.counter -=1
                    self.currentWorkers.remove(td)
                    self.currentQtdWorkers-=1
                    print("releasing thread")
        if(self.counter == 0 and not self.pool and not self.currentWorkers):
            self.state = State.DONE
            


