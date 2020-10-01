# -*- coding: utf-8
import os
import sys

import requests
import io
import json
import signin
import time

if __name__ == '__main__':
	
    if sys.getdefaultencoding() != 'utf-8':
        reload(sys)
        sys.setdefaultencoding('utf-8')
	print '=== '+time.strftime("%Y-%m-%d")+'日签到情况'+' ==='
    # ('18725345157', '1757472335dwg')#段旺国
    # ('15974520434', 'zhangyuce1997gc')#张愉策
    # ('18468275515', 'W679860679860J')#王建
    signin = signin.Signin("", "", "")
    # data = io.open("/www/wwwroot/yiban_test_server2.7/studentinfo.json", encoding="UTF-8")
    data = io.open("./studentinfo.json", encoding="UTF-8")
    strJson = json.load(data)
    i = 0
    j = 0
    for x in strJson:
        i = i + 1
    while j < i:
        j = j + 1
        user = strJson[str(j)]["user"]
        pasw = strJson[str(j)]["pasw"]
        addr = strJson[str(j)]["addr"]
        user=user.replace(" ","")
        pasw=pasw.replace(" ","")
        add=strJson[str(j)]["add"]
        # addr=addr.replace(" ","")
        uid = strJson[str(j)]["uid"]  # wx

        signin.account = user
        signin.passwd = pasw
        signin.uid = uid
        if (signin.login()):
            signin.getLocation()
            signin.getuncompletedList(add,addr)
        print('\n\n')
    data.close()
