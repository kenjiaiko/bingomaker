#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import random
import shutil
import json
import cgi
import cv2

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
	imageid = random.randint(100000000, 999999999)
	baseurl = status["local_pics_path"] + userid + "/" + str(imageid)
	os.mkdir(baseurl)
	save_jpg_for_size(img, 305, baseurl)
	return status["web_pics_path"] + userid + "/" + str(imageid)

def html(text):
	print "Content-Type: application/json"
	print
	print "{'result': '" + text + "'}"
	sys.exit()

def main():
	form = cgi.FieldStorage()
	try:
		num = form.getvalue("num")
	except:
		html('404 not found')
	if num == None:
		html('404 not found')
	num = int(num)
	uid = random.randint(100000000, 999999999)
	data= {
		'data': [],
		'result': 'ok'
	}
	for i in range(num):
		bingo = new_bingo(75)
		url   = make_imagemap_from_data(str(uid), bingo, [99])
		one = {
			"url":  url,
			"data": bingo
		}
		data['data'].append(one)
	print "Content-Type: application/json"
	print
	print json.dumps(data, indent=4)

if __name__ == '__main__':
	main()

