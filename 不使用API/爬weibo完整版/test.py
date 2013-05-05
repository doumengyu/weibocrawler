#! /usr/bin/env python
#coding=utf-8
import time
import datetime

if __name__ == '__main__':
    s = datetime.datetime(2012,9,1)
    
    print time.mktime(s.timetuple())
    