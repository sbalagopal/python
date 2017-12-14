#!/usr/bin/python

import threading
import requests
import random
import urllib
import time


URL = 'http://192.168.1.201/wsgi/hello.wsgi'
MAX_THREADS = 10
TIME_TO_RUN = 60 * 5

starttime = time.time()


def get_url(URL):
    #sw = rand_search_string()
    #a = requests.get(URL % urllib.quote_plus(sw))
    a = requests.get(URL)
    print "Response time (ms): %s\n" % (a.elapsed.total_seconds()*1000)

def rand_search_string():
    sw_text = open('actors.txt','rb').read()
    sw_list = sw_text.split('\n')
    list_len = len(sw_list)

    index = random.randrange(0,list_len)
    return sw_list[index]


while True:
    time_alive = time.time() - starttime
    if time_alive >= TIME_TO_RUN:
        time.sleep(10)
        print "Its been %s min since I started. Exiting" % (TIME_TO_RUN/60)
        break
    if threading.activeCount() >= MAX_THREADS:
        continue
    t = threading.Thread(target=get_url, args=(URL,))
    t.start()
    #print threading.activeCount(), time_alive

