#!/usr/bin/python
# -*- coding: utf-8 -*-

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

def main(n, ip):
	path = "numbers/"
	nums = {}
	rndN = [ i for i in range(25) ]
	imgs = []
	for name in os.listdir(path):
		nums.setdefault(int(name[5:7]), cv2.imread(path + name))
	status = json.loads(open("status.json").read())
	a = time.time()
	r = requests.get("http://" + ip + "/" + status["cgi_path"] + "?num=" + str(n), timeout=6.0)
	data = r.json()
	for d in data["data"]:
		r = requests.get("http://" + ip + "/" + d["url"] + "/305.jpg", timeout=6.0)
		imgs.append( [cv2.imdecode(np.asarray(bytearray(r.content), dtype=np.uint8), -1), d["data"]] )
	result_time = time.time() - a
	random.shuffle(imgs)
	imgs = imgs[:100]
	all_nums = {}
	for i in range(75):
		all_nums.setdefault(i+1, 0)
	all_nums.setdefault(99, 0)
	db = pysql.sql("bingo.db")
	db_bingo_list = []
	db_bingo_list_same_checker = []
	for (img, b) in imgs:
		for i in b:
			all_nums[i] += 1
		for row in db.read(str(b)):
			is_exist = row[0]
			break
		if 0 < is_exist:
			db.close()
			return 1001.0
		db_bingo_list.append( (ip, str(b), int(time.time())) )
		db_bingo_list_same_checker.append(str(b))
	if len(db_bingo_list_same_checker) != len(set(db_bingo_list_same_checker)):
		db.close()
		return 1000.0
	all_nums_list = sorted(all_nums.items(), key=lambda x:x[1], reverse=True)
	nums_sub = all_nums_list[1][1] - all_nums_list[-1][1] # 2nd - 75th (1st is 99)
	if nums_sub < 11 or 40 < nums_sub:
		db.close()
		return 999.0
	for (img, b) in imgs:
		random.shuffle(rndN)
		for i in rndN[:1]:
			#print is_same(img, (i / 5) + 1, (i % 5), nums[b[i]])
			if 50000 < is_same(img, (i / 5) + 1, (i % 5), nums[b[i]]):
				db.close()
				return 998.0
	db.insert(db_bingo_list)
	db.commit()
	db.close()
	return result_time

def test(count, limit_time, ip, test_flag=True):
	if test_flag == True:
		sflag = main(count, ip)
	else:
		try:
			sflag = main(count, ip)
		except:
			sflag = 997.0
	if limit_time < sflag:
		print "failed",
	else:
		print "success",
	print sflag

if __name__ == '__main__':
	teamip= sys.argv[1]
	count = int(sys.argv[2])
	test(count, 5.0, teamip, False)

