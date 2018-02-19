#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

def main():
	result = {}
	path   = "result/"
	for name in os.listdir(path):
		num = float(open(path + name).read())
		result.setdefault(name, 0.0)
		result[name] = num
	for k, v in sorted(result.items(), key=lambda x:x[1])[:1]:
		open("exec/" + k, "w").write("TOP")

if __name__ == '__main__':
	os.chdir(os.path.abspath(os.path.dirname(__file__)))
	main()

