AutoSleep
=========

Suspend (SIGSTOP) processes which are not needed when system runs on battery. Resume (SIGCONT) processes once they are needed again.

For Chrome: All processes which belongs to tabs in the background can be stopped.

In general, if an app is in the background and not an important system service, it can be stopped.

Also see [chrome-suspender.py](https://github.com/albertz/system-tools/blob/master/bin/chrome-suspender.py).
