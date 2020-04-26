#!/usr/bin/env python
# WebPwn3r is a Web Applications Security Scanner
# By Ebrahim Hegazy - twitter.com/zigoo0
# First demo conducted 12Apr-2014 @OWASP Chapter Egypt
# https://www.owasp.org/index.php/Cairo
import sys
import threading
from  multiprocessing import Process, Pool
from Queue import Queue

from vulnz import *
from headers import *


thread_queue = []

def CheckVul(url):
	small_list = []
	threads = [rce_func, xss_func, error_based_sqli_func]
	for i in threads:
		small_list.append(threading.Thread(target=i, args=(url,)))
	
	for thread in small_list:
		thread.start()

	for thread in small_list:
		thread.join(timeout=60)
	

def MakeQueue(file):
	open_list = open(file).readlines()
	for link in open_list:
		if "?" in link:
			url = link.strip()
			thread_queue.append(url)

if __name__ == "__main__":
	MakeQueue(sys.argv[1])

	s = Pool(10)
	s.map(CheckVul,thread_queue)
		