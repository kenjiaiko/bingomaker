#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json
import os
import requests

def get_data_from_users(ip):
	status = json.loads(open("status.json").read())
	# step1
	r = requests.get("http://" + ip + "/" + status["cgi_path"] + "?num=" + str(100))
	d = r.json()
	if len(d["data"]) != 100:
		return True
	for v in d["data"]:
		r = requests.get("http://" + ip + "/" + v["url"] + "/305.jpg")
		if r.status_code != requests.codes.ok:
			return True
	# step2
	call_number = d["data"][0]["data"][0]
	game_id     = d["data"][0]["url"].split("/")[1]
	r = requests.get("http://" + ip + "/" + status["cgi_path"] + "?uid=" + game_id + "&call=" + str(call_number))
	d = r.json()
	if len(d["data"]) != 100:
		return True
	r = requests.get("http://" + ip + "/" + d["data"][0]["url"] + "/305.jpg")
	if r.status_code != requests.codes.ok:
		return True
	return False

def main(ip):
	r = get_data_from_users(ip)
	if r == True:
		print "error"
	else:
		print "success"

if __name__ == '__main__':
	# sys.argv[1] = ip address
	i = 5
	while 0 < i:
		main(sys.argv[1])
		i -= 1

