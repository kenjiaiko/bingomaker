#!/usr/bin/python
# -*- coding: utf-8 -*-

USER_TIMEOUT   = 60.0
SYSTEM_TIMEOUT = 120.0

import sys
import os
import json
import time
import requests
import random
import cv2
import numpy as np

import pysql

def _x(a, b):
	if a < b:
		return b-a
	return a-b

def is_same(a, pos_h, pos_w, b):
	diff = 0
	for h in range(61):
		for w in range(61):
			(r1, g1, b1) = a[61 * pos_h + h, 61 * pos_w + w]
			(r2, g2, b2) = b[h, w]
			diff += _x(r1, r2)
			diff += _x(g1, g2)
			diff += _x(b1, b2)
	return diff

def get_data_from_users(n, ip, limi):
	imgs = []
	status = json.loads(open("status.json").read())
	a = time.time()
	# step1
	r = requests.get("http://" + ip + "/" + status["cgi_path"] + "?num=" + str(n), allow_redirects=False)
	d = r.json()
	if len(d["data"]) != n:
		return None
	random.shuffle(d["data"])
	i = 0
	for v in d["data"]:
		r = requests.get("http://" + ip + "/" + v["url"] + "/305.jpg", allow_redirects=False)
		if i < 100:
			imgs.append( [cv2.imdecode(np.asarray(bytearray(r.content), dtype=np.uint8), -1), v["data"]] )
		i += 1
	# step2
	calling_numbers = [ i+1 for i in range(75) ]
	random.shuffle(calling_numbers)
	called_imgs = []
	for c in calling_numbers[:5]:
		target = random.randint(0, len(d["data"]) - 1)
		r = requests.get("http://" + ip + "/" + status["cgi_path"] + "?uid=" + d["data"][target]["url"].split("/")[1] + "&call=" + str(c))
		d = r.json()
		if len(d["data"]) != n:
			return None
		r = requests.get("http://" + ip + "/" + d["data"][target]["url"] + "/305.jpg", allow_redirects=False)
		called_imgs.append( [cv2.imdecode(np.asarray(bytearray(r.content), dtype=np.uint8), -1), d["data"][target]["data"]] )
	b = time.time() - a
	return (b, imgs, called_imgs, calling_numbers)

def check1(db, imgs, the_numbers, ip):
	bl = []
	ck = []
	for (img, b) in imgs:
		for i in b:
			the_numbers[i] += 1
		for row in db.read(str(b)):
			is_exist = row[0]
			break
		if 0 < is_exist:
			return None
		bl.append( (ip, str(b), int(time.time())) )
		ck.append(str(b))
	if len(ck) != len(set(ck)):
		return 2001.0
	ranking = sorted(the_numbers.items(), key=lambda x:x[1], reverse=True)
	diff275 = ranking[1][1] - ranking[-1][1] # 2nd - 75th (1st is 99)
	if diff275 < 11 or 40 < diff275:
		return 2002.0
	return bl

def check2(imgs, nums):
	for (img, b) in imgs:
		pos = random.randint(0, 24)
		if 50000 < is_same(img, (pos / 5) + 1, (pos % 5), nums[b[pos]]):
			return 3001.0
	return None

def check3(imgs, calling_numbers, blue_nums, gray_nums):
	called_nums = []
	for (img, b) in imgs:
		pos = random.randint(0, 24)
		called_nums.append(calling_numbers.pop(0))
		if b[pos] in called_nums:
			if 50000 < is_same(img, (pos / 5) + 1, (pos % 5), gray_nums[b[pos]]):
				return 4001.0
		else:
			if 50000 < is_same(img, (pos / 5) + 1, (pos % 5), blue_nums[b[pos]]):
				return 4001.0
	return None

def error(r, db=None):
	if db != None:
		db.close()
	return r

def timeout(msg):
	failed(9998.0)

from pytimeout import on_timeout
@on_timeout(limit=SYSTEM_TIMEOUT, handler=timeout)
def main(n, ip):
	path = "numbers/"
	#
	# get a data from user's server
	#
	r = get_data_from_users(n, ip, 10.0)
	if r == None:
		return 1001.0
	(result, imgs, called_imgs, calling_numbers) = r
	#
	# check a data from user's server
	#   check only 100 data for peformance
	# 
	the_numbers = {}
	for i in range(75):
		the_numbers.setdefault(i+1, 0)
	the_numbers.setdefault(99, 0)
	# check1
	db = pysql.sql("db/" + ip + ".db")
	r = check1(db, imgs, the_numbers, ip)
	if type(r) == float:
		return error(r, db)
	db_update_data = r
	# check2
	blue_nums = {}
	gray_nums = {}
	for name in os.listdir(path):
		if name.find("blue_") == 0 or name == "gray_99.jpg":
			blue_nums.setdefault(int(name[5:7]), cv2.imread(path + name))
		else:
			gray_nums.setdefault(int(name[5:7]), cv2.imread(path + name))
	r = check2(imgs, blue_nums)
	if type(r) == float:
		return error(r, db)
	# check3
	r = check3(called_imgs, calling_numbers, blue_nums, gray_nums)
	if type(r) == float:
		return error(r, db)
	# update db
	db.insert(db_update_data)
	db.commit()
	db.close()
	return result

# for output to "result/"
g_teamip = ""

def failed(sflag):
	global g_teamip
	#print "failed", sflag
	open("result/" + g_teamip, "w").write(str(sflag))
	sys.exit()

def success(sflag):
	global g_teamip
	#print "success", sflag
	open("result/" + g_teamip, "w").write(str(sflag))
	sys.exit()

def test(count, limit_time, ip, test_flag=True):
	if test_flag == True:
		sflag = main(count, ip)
	else:
		try:
			sflag = main(count, ip)
		except:
			sflag = 9999.0
	if limit_time < sflag:
		failed(sflag)
	else:
		success(sflag)

if __name__ == '__main__':
	os.chdir(os.path.abspath(os.path.dirname(__file__)))
	teamip   = sys.argv[1]
	g_teamip = sys.argv[1]
	count    = 100
	execpath = "exec/" + teamip
	try:
		data = open(execpath).read()
	except:
		data = None
	if data != None:
		os.remove(execpath)
		test(count, USER_TIMEOUT, teamip, False)

