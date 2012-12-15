#!/usr/bin/python

from pprint import pprint
import psutil
import os

pslist = psutil.get_process_list()

def hasAccess(p):
	try: p.exe
	except psutil.error.AccessDenied: return False
	return True

pslist = filter(hasAccess, pslist)

for p in pslist:
	#print p.pid, p.name, str(p.status)
	if p.status != psutil.STATUS_STOPPED: continue
	print "resuming:", p.pid, p.name
	p.resume()
