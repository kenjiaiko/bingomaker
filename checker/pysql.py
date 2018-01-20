#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import sqlite3

class sql(object):
	
	def __init__(self, filepath):
		self.conn = sqlite3.connect(filepath)
		self.c = self.conn.cursor()
	
	def cmd(self, q, data=None):
		if data == None:
			r = self.c.execute(q)
		else:
			r = self.c.executemany(q, data)
		return r
	
	def create(self):
		self.cmd('create table bingos (teamid text, bingo text, t integer);')
		self.cmd('create index bingoindex on bingos(bingo);')
	
	def insert(self, data):
		self.cmd('insert into bingos (teamid, bingo, t) values (?,?,?);', data)
	
	def commit(self):
		self.conn.commit()
	
	def close(self):
		self.conn.close()
	
	def read(self, bingo):
		return self.cmd('select count(bingo) from bingos where bingo="' + str(bingo) + '";')

if __name__ == '__main__':
	data = []
	db = sql("bingo.db")
	db.create()
	db.close()

