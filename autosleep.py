#!/usr/bin/python

from pprint import pprint
import psutil # easy_install psutil
import os

pslist = psutil.get_process_list()

def hasAccess(p):
	try: p.exe
	except psutil.error.AccessDenied: return False
	return True

pslist = filter(hasAccess, pslist)

def printProclist(plist):
	for p in plist:
		print p.pid, p.name, p.exe

def isSystemLauncher(p):
	if p.pid in [0,1]: return True
	if p.exe == "/sbin/launchd": return True
	if p.exe == "/sbin/init": return True
	if p.exe == "/bin/init": return True
	return False

def isTopLevel(p):
	if isSystemLauncher(p.parent): return True
	return False

toplevelProclist = filter(isTopLevel, pslist)
#printProclist(toplevelProclist)

foregroundProc = None

def isImportantSystemService(p):
	if isSystemLauncher(p): return True
	# maybe too much but not sure how to do otherwise...
	if p.exe.startswith("/sbin/"): return True
	if p.exe.startswith("/usr/sbin/"): return True
	if p.exe.startswith("/usr/libexec/"): return True
	if p.exe.startswith("/System/"): return True
	return False

blacklistBasename = [
	"fish", "bash",	"zsh",
	"fishd",
	"ssh-agent",
	"MusicPlayer", # more intelligent, only if playing?
	"Terminal", # we could screw ourself while debugging :p
]
def shouldSleep(p):
	if isImportantSystemService(p): return False
	if os.path.basename(p.exe) in blacklistBasename: return False
	return True

def suspendProc(p):
	p.suspend()
	for childp in p.get_children():
		suspendProc(childp)

def hasVisibleWindows(p):
	global appscript_sysev
	if "appscript_sysev" in globals():
		sysev = appscript_sysev
	else:
		import appscript
		sysev = appscript.app("System Events")
		appscript_sysev = sysev
	def appByPid(pid):
		l = [p for p in sysev.application_processes() if p.unix_id() == 285]
		assert len(l) <= 1
		if l: return l[0]
		return None
	app = appByPid(p.pid)
	if not app: return False
	if not app.visible(): return False
	wins = app.windows()
	if not wins: return False
	if any([w.attributes['AXMinimized'].value() for w in wins]): return True
	return False
	
for p in toplevelProclist:
	if p.status == psutil.STATUS_STOPPED: continue # already sleeping
	if not shouldSleep(p): continue
	if hasVisibleWindows(p): continue
	print "suspend", p.pid, p.name
	suspendProc(p)

#printProclist(filter(shouldSleep, toplevelProclist))
	
#pprint([p for p in psutil.get_process_list() if p.status == psutil.STATUS_STOPPED])

