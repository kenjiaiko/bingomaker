#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps

def on_timeout(limit, handler):
	def notify_handler(signum, frame):
		handler("timeout: " + str(signum))
	def __decorator(function):
		def __wrapper(*args, **kwargs):
			import signal
			signal.signal(signal.SIGALRM, notify_handler)
			signal.alarm(int(limit))
			r = function(*args, **kwargs)
			signal.alarm(0)
			return r
		return wraps(function)(__wrapper)
	return __decorator

