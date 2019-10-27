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
from myThreadPool import MyThreadPool, State
is_py2=sys.version[0] == '2'
if is_py2:
    from Queue import Queue as Queue
else:
    from queue import Queue as Queue