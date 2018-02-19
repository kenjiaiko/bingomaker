#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import cgi
import time

def _html(ip, path):
	path += ip
	try:
		t = str(open(path).read())
	except:
		t = str(10000.0)
	print "Content-Type: text/html"
	print
	print "<html>"
	print "<body>"
	print "<p>" + ip + "</p>"
	print "<p>Response Time: " + t + "</p>"
	print '<p><input type="button" value="Measure" onclick="location.href=\'index.cgi?check\'"></p>'
	print "<ol>"
	print '<li>The Raspberry Pi distributed to each team contains the Bingo-Service program'
	print '<li>Please log-in your Raspberry Pi ( ssh: ' + ip + ', user/pass = pi/kenjiinwonderland )'
	print '<li>Please set up Bingo-Service on ' + ip + ' : 80'
	print '<li>If you click "Measure" button above, the system will accesses your Bingo-Service in a few minutes later'
	print '<li>"Measure" button can be clicked once every 7 minutes (Once you click it, you have to wait for 7 minutes)'
	print '<li>Even if you do not click "Measure" button, the system may occasionally access your Bingo-Service'
	print '<li>Response time of your service is measured'
	link_url = '<a href="flag.cgi">flag.cgi</a>'
	print '<li>The hash of the team with the shortest response time is automatically written to ' + link_url
	print '<li>In this challenge, players do not need to write "Team Hash" on a regular basis'
	print '</ol>'
	print "</body>"
	print "</html>"
	sys.exit()

def err(txt):
	print "Content-Type: text/html"
	print
	print txt
	sys.exit()

def main():
	octs = os.environ['REMOTE_ADDR'].split(".")
	ip   = octs[0] + "." + octs[1] + "." + octs[2] + "." + "254"
	try:
		n = int(open("tmp/" + ip).read())
	except:
		n = 0
	now_time = int(time.time())
	# --
	if os.environ.get("QUERY_STRING", "No Query String in url") == "check":
		limt = 60 * 7
		if (n + limt) < now_time:
			open("tmp/" + ip, "w").write(str(now_time))
			open("exec/" + ip, "w").write(str(now_time))
			err("The system will access " + ip + " within some minutes.")
		else:
			err("Wait: " + str( (n + limt) - now_time ) + "(s)")
	else:
		path = "result/"
		_html(ip, path)

if __name__ == '__main__':
	main()

