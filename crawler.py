 # -*- coding: ISO-8859-1 -*-
import threading
import urllib.request
import re
from bs4 import BeautifulSoup
import requests
import os
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
import sys
import time
is_py2=sys.version[0] == '2'
if is_py2:
    from Queue import Queue as Queue
else:
    from queue import Queue as Queue

class State(Enum):
    WAITING = 0
    RUNNING = 1
    DONE = 2
class ImageDownloader:
    def prepareExecution(self):
        if self.prepared == State.WAITING:
            self.prepared = State.RUNNING
            try:
                with open (self.urls, 'r') as urls:
                    line = urls.readline()
                    while line:
                        self.prepared = State.RUNNING
                        worker = self.threadPool.submit(self.getImageUrls, line)
                        print('******************')
                        self.startFutures.add(worker)
                        worker.add_done_callback(self.crawlerCallback)
                        print(line)
                        line =  urls.readline()
                        
            except Exception as e:
                print (e)
            finally:
                urls.close()

    def __init__(self, param1):
        self.urls = param1
        self.threadList=[]
        self.threadPool = ThreadPoolExecutor(max_workers=20)
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
            print("nao foi possivel realizar o download da imagem " + str(url))
            
    def getImageUrls(self, urll):
        srcImage = ''
        with urllib.request.urlopen(urll) as url:
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
                self.to_crawl.put(srcImage)     

    
    def crawlerCallback(self, res):
        result = res.result()
        if result and result.status_code == 200:
            print(result)

    def stillLoadingURLImages(self):
        if self.prepared != State.DONE:
            for job in self.startFutures:
                '''Verifica se as threads iniciais (dos links das imagens) ainda está rodando!
                Se ainda estiver rodando então o loop na função start() deve continuar iterando!'''
                if job.running():
                    return True
            self.prepared = State.DONE
        return False

    def start(self):
        self.prepareExecution()
        while not(self.to_crawl.empty()) or self.stillLoadingURLImages():
            try:
                current_url=self.to_crawl.get(timeout=60)
                if current_url and current_url not in self.readUrls:
                    self.readUrls.add(current_url)
                    #vai para o pool de threads concorrer pelo bastão para a execução!
                    worker = self.threadPool.submit(self.download, current_url)
                    #Finaliza o processo, e desaloca o 'bastão' do processo
                    #A lib threadPool do python utiliza lock e mutex para tratar a concorrência
                    worker.add_done_callback(self.crawlerCallback)
            except Exception as e:
                print(e)

if __name__ == "__main__":
    #passa o nome do arquivo por parâmetro
    archive = sys.argv[1:]
    if archive:
        imgDownloader = ImageDownloader(archive[0])
        imgDownloader.start()
    else:
        print("Por favor informe o nome do arquivo que possui os links!")
