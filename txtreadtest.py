#!/usr/bin/python  
# -*- coding: UTF-8 -*-
# import sys
# reload(sys)

f = open("sample.txt", 'r')
line = f.readlines()
print line
i=0
while i<len(line):
    xy= line[i].split(",")
    lng0 = xy[0]
    lat0 = xy[1]
    i=i+1

f.close()