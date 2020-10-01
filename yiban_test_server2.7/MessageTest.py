# -*- coding: utf-8
import time
import json
import requests

'''
微信推送
'''
url='xxx'
appToken='xxx'


def sendMessWx(uid):

    content =time.strftime("%Y-%m-%d")+'易班自动签到完成！——感谢使用！'
    url = 'http://wxpusher.zjiecode.com/api/send/message/?appToken=' + appToken + '&content=' + content + '&uid=' + uid
    res=requests.get(url)
    print (res.text)
    
 
def sendMessWx2(uid, url):
    content = time.strftime("%Y-%m-%d") + '自动打卡完成 详情查看：' + str(url)
    url = 'http://wxpusher.zjiecode.com/api/send/message/?appToken=' + appToken + '&content=' + content + '&uid=' + uid
    res = requests.get(url)
    print (res.text)

def sendMessWxInfo(uid, info):
    url = 'http://wxpusher.zjiecode.com/api/send/message/?appToken=' + appToken + '&content=' + info + '&uid=' + uid
    res = requests.get(url)
    print (res.text)

def SendMessWxPost(uid,url2):
    head = {"Content-Type": "application/json; charset=UTF-8", 'Connection': 'close'}
    content = time.strftime("%Y-%m-%d") + '自动打卡完成 详情点击链接查看哦:'
    data2 = {
        "appToken": appToken,
        "content": content,
        "contentType": 1,
        "uids": [
            uid
        ],
        "url": url2
    }
    r = requests.post(url, data=json.dumps(data2), headers=head)
    print r.text

