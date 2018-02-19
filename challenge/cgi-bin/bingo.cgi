#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import random
import json
import cgi
import cv2

def rnd(digit):
	s = ""
	for i in range(digit):
		s += str(random.randint(0, 9))
	return s

def new_bingo(max_number=75):
	num_base = []
	if max_number == 75:
		I15 = [i+1 for i in range( 0, 15)]
		I30 = [i+1 for i in range(15, 30)]
		I45 = [i+1 for i in range(30, 45)]
		I60 = [i+1 for i in range(45, 60)]
		I75 = [i+1 for i in range(60, 75)]
		random.shuffle(I15)
		random.shuffle(I30)
		random.shuffle(I45)
		random.shuffle(I60)
		random.shuffle(I75)
		for i in range(5):
			num_base.append(I15[i])
			num_base.append(I30[i])
			num_base.append(I45[i])
			num_base.append(I60[i])
			num_base.append(I75[i])
	else:
		for i in range(max_number):
			num_base.append(i+1)
		random.shuffle(num_base)
	num_base[12] = 99
	return num_base[:25]

def check_bingo(bingo, called_nums):
	ck_list = [
		# yoko
		[ 0, 1, 2, 3, 4],
		[ 5, 6, 7, 8, 9],
		[10,11,12,13,14],
		[15,16,17,18,19],
		[20,21,22,23,24],
		# tate
		[ 0, 5,10,15,20],
		[ 1, 6,11,16,21],
		[ 2, 7,12,17,22],
		[ 3, 8,13,18,23],
		[ 4, 9,14,19,24],
		# naname
		[ 0, 6,12,18,24],
		[ 4, 8,12,16,20]
	]
	for ck in ck_list:
		flag = True
		for i in range(5):
			if not bingo[ck[i]] in called_nums:
				flag = False
				break
		if flag == True:
			return 1
	return 0

def save_jpg_for_size(original, size, baseurl):
	cv2.imwrite(baseurl + "/" + str(size) + ".jpg", original)

def make_imagemap_from_data(userid, bingo, called_nums):
	card = [cv2.imread("bingotitle.jpg")]
	for i in range(5):
		line_ = []
		for j in range(5):
			n = bingo[ (i * 5) + j ]
			if not n in called_nums:
				one = cv2.imread("numbers/blue_" + ("%02d" % n) + ".jpg")
			else:
				one = cv2.imread("numbers/gray_" + ("%02d" % n) + ".jpg")
			line_.append(one)
		card.append(cv2.hconcat(line_))
	img = cv2.vconcat(card)
	status  = json.loads(open("status.json").read())
	baseurl = status["local_pics_path"] + userid
	if os.path.isdir(baseurl) == False:
		os.mkdir(baseurl)
	imageid = rnd(20)
	baseurl = status["local_pics_path"] + userid + "/" + imageid
	os.mkdir(baseurl)
	save_jpg_for_size(img, 305, baseurl)
	return status["web_pics_path"] + userid + "/" + imageid

def html(text):
	print "Content-Type: application/json"
	print
	print "{'result': '" + text + "'}"
	sys.exit()

def branch():
	form = cgi.FieldStorage()
	num  = form.getvalue("num")
	if num != None:
		return (0, num)
	uid  = form.getvalue("uid")
	call = form.getvalue("call")
	if uid != None and call != None:
		return (1, uid, call)
	return (-1, "error")

def main():
	result = branch()
	if result[0] == 0:
		routineA(result[1])
		return
	if result[0] == 1:
		routineB(result[1], result[2])
		return
	html("404 not found")
	return

def routineA(num):
	if num == None:
		html('404 not found')
	if int(num) < 1:
		html('404 not found')
	num = int(num)
	uid = rnd(30)
	data= {
		'data': [],
		'result': 'ok',
		'called': [99]
	}
	for i in range(num):
		bingo = new_bingo(75)
		url   = make_imagemap_from_data(uid, bingo, [99])
		one = {
			"url":  url,
			"data": bingo
		}
		data['data'].append(one)
	path = json.loads(open("status.json").read())["local_pics_path"] + uid + "/" + "ginfo.json"
	open(path, "w").write(json.dumps(data, indent=4))
	print "Content-Type: application/json"
	print
	print json.dumps(data, indent=4)

def routineB(uid, call):
	path = json.loads(open("status.json").read())["local_pics_path"] + uid + "/" + "ginfo.json"
	ginfo= json.loads(open(path).read())
	if not int(call) in ginfo["called"]:
		ginfo["called"].append(int(call))
		data = {
			'data': [],
			'result': 'ok',
			'called': ginfo["called"]
		}
		for v in ginfo["data"]:
			url = make_imagemap_from_data(uid, v["data"], ginfo["called"])
			one = {
				"url": url,
				"data": v["data"],
				"bingo": check_bingo(v["data"], ginfo["called"])
			}
			data['data'].append(one)
		open(path, "w").write(json.dumps(data, indent=4))
	else:
		data = ginfo
	print "Content-Type: application/json"
	print
	print json.dumps(data, indent=4)

if __name__ == '__main__':
	main()

