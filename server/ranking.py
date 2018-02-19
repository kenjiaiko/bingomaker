#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def main():
	result = {}
	path   = "result/"
	for name in os.listdir(path):
		num = float(open(path + name).read())
		result.setdefault(name, 0.0)
		result[name] = num
	for k, v in sorted(result.items(), key=lambda x:x[1]):
		print k, v

if __name__ == '__main__':
	main()

