 # -*- coding: ISO-8859-1 -*-
from threading import Thread
import urllib.request
import re
from bs4 import BeautifulSoup
import requests
import os
from concurrent.futures import ThreadPoolExecutor
import sys
import time
from myThreadPool import MyThreadPool
from state import State
import logging

is_py2=sys.version[0] == '2'
if is_py2:
    from Queue import Queue as Queue
else:
    from queue import Queue as Queue


class ImageDownloader:
    def prepareExecution(self):
        if self.prepared == State.WAITING:
            self.prepared = State.RUNNING
            try:
                with open (self.urls, 'r') as urls:
                    line = urls.readline()
                    while line:
                        self.prepared = State.RUNNING
                        self.threadPool.submit(self.getImageUrls, line)
                        print(line)
                        line =  urls.readline()
                        
            except Exception as e:
                print (e)
            finally:
                urls.close()

    def __init__(self, param1):
        self.urls = param1
        self.threadList=[]
        self.threadPool = MyThreadPool(20)
        self.readUrls = set([])
        self.to_crawl = Queue()
        self.prepared = State.WAITING
        self.startFutures = set([])
        if(not(os.path.exists("downloaded photos"))):
            os.mkdir('./downloaded photos')
    
    def download(self, url):
        try:
            if(not("http" in url)):
                url="http:"+url
            r = requests.get(url)
            
            namePath="./downloaded photos/"+str(url).split('/').pop()
            with open (namePath, 'wb') as f:
                f.write(r.content)
        except:
            loggin.warning("nao foi possivel realizar o download da imagem " + str(url))
            
    def getImageUrls(self, urll):
        srcImage = ''
        with urllib.request.urlopen(urll) as url:
            try:
                htmltext = url.read()
                soup = BeautifulSoup(htmltext, "html.parser")
                images = []
                images = soup('img')

                for image in images:
                    if(image.get('src') != None):
                        srcImage = image.get('src')
                    elif(image.get('data-src')):
                        srcImage = image.get('data-src')
                    else:
                        srcImage = ''
                    self.threadPool.mutex.acquire()
                    self.to_crawl.put(srcImage)  
                    self.threadPool.mutex.release()
                    
                      
            except Exception as e:
                print(e)


    def start(self):
        self.prepareExecution()

        execThread = Thread(target = self.threadPool.run, args=())
        execThread.start()
        
        while self.threadPool.state is not State.DONE:
            try:
                current_url=self.to_crawl.get(timeout=60)
                if current_url and current_url not in self.readUrls:
                    self.readUrls.add(current_url)
                    #vai para o pool de threads concorrer pelo bastão para a execução!
                    self.threadPool.submit(self.download, current_url)
                    
            except Exception as e:
                logging.warning(e)
        
        

if __name__ == "__main__":
    #passa o nome do arquivo por parâmetro
    archive = sys.argv[1:]
    if archive:
        imgDownloader = ImageDownloader(archive[0])
        imgDownloader.start()
    else:
        logging.info("Por favor informe o nome do arquivo que possui os links!")
