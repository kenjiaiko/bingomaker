#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import socket

def ip2hash(ip):
	return ip

def main():
	result = {}
	path   = "result/"
	for name in os.listdir(path):
		num = float(open(path + name).read())
		result.setdefault(name, 0.0)
		result[name] = num
	print "Content-Type: text/html"
	print
	print "<html>"
	print "<body>"
	for k, v in sorted(result.items(), key=lambda x:x[1])[:1]:
		print "<p>" + ip2hash(k) + "</p>"
		print "<p>Response Time: " + str(v) + "</p>"
	print "</body>"
	print "</html>"

if __name__ == '__main__':
	main()

