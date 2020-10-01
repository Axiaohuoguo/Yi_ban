# -*- coding: utf-8
import json
import time
from json import dumps
import MessageTest

import requests
import util


class Signin:
    CSRF = "duan-wang-guo"
    COOKIES = {"csrf_token": CSRF}
    HEADERS = {"Origin": "https://c.uyiban.com", "User-Agent": "yiban_android"}

    def __init__(self, account, passwd, uid):
        self.account = account
        self.passwd = passwd
        self.uid = uid
        self.session = requests.session()
        self.cookies = requests.cookies.RequestsCookieJar()
        self.token = "";
        self.access_token = "";
        self.PHPSESSID = ""
        self.s = ""
        self.TaskId = ""  # 任务id
        self.cpi = ""

    def request(self, url, method="get", params=None, cookies=None):
        req = self.session.get(url, params=params, timeout=10, headers=self.HEADERS, cookies=cookies)
        try:
            # print(req.json())
            # MessageTest.sendMessWxInfo(self.uid, "您提供的账号或密码有误，无法登录，请联系我更正")
            return req.json()
        except:
            return None

    # 登录
    def login(self):
        print("================登录================")
        params = {
            "account": self.account,
            "ct": 2,
            "identify": 0,
            "v": "4.7.5",
            "passwd": util.encrypt_passwd(self.passwd)
        }
        r = self.request(url="https://mobile.yiban.cn/api/v2/passport/login", params=params)
        if r is not None:
            try:
                self.access_token = r["data"]["access_token"]
                self.token = r["data"]["token"]
            except KeyError:
                print self.account + "  [ERROR]登录结果： 账号或密码错误!"
                MessageTest.sendMessWxInfo(self.uid, "[ERROR]您提供的账号或密码有误请联系我更正！！")
                return False
            pass
        print self.account + "  [OK]登录结果： 成功！"
        return True

    def getLocation(self):
        url = "http://f.yiban.cn/iapp/index?act=iapp7463&v="
        cookies = {
            "loginToken": self.token
        }
        r = self.session.get(url=url + self.access_token, headers=self.HEADERS, cookies=cookies, allow_redirects=False)
        # print(r.headers["Location"])
        Location = str(r.headers["Location"])
        verify_request = Location[Location.find("verify_request=") + 15:Location.find("&")]
        # print("================verify_request================")
        # print(verify_request);
        # yb_uid = "";
        url = "https://api.uyiban.com/base/c/auth/yiban";
        params = {
            "verifyRequest": verify_request,
            "CSRF": self.CSRF
        }
        cookies = {
            "csrf_token": self.CSRF
        }
        headers = {
            "Origin": "https://c.uyiban.com",
            "User-Agent": "yiban_android"
        }
        rr = requests.get(url=url, params=params, cookies=cookies, headers=headers)
        # print("================Get-PHPSESSID================")
        Set_Cookie = str(rr.headers["Set-Cookie"])
        # print(Set_Cookie)
        self.PHPSESSID = Set_Cookie[Set_Cookie.find("=") + 1:Set_Cookie.find(";")]
        # print(self.PHPSESSID)
        print("================cip================")
        self.cpi = Set_Cookie[Set_Cookie.find("cpi=") + 4:Set_Cookie.find("%3D%3D;") + 6]
        # print(self.cpi)

    # 获得未完成清单
    def getuncompletedList(self, add, addr):
        url = "https://api.uyiban.com/officeTask/client/index/uncompletedList";
        params = {
            "StartTime":str(time.strftime('%Y-%m-%d',time.localtime(time.time()-86400*7)))+" 00:00",
            "EndTime":str(time.strftime('%Y-%m-%d',time.localtime(time.time())))+" 23:59",
            "CSRF": self.CSRF
        }
        cookies = {
            "csrf_token": self.CSRF,
            "PHPSESSID": self.PHPSESSID,
            "cpi": "BB=="
        }
        headers = {
            "Origin": "https://app.uyiban.com",
            "User-Agent": "yiban_android"
        }
        re = self.session.get(url=url, params=params, headers=headers, cookies=cookies)
        re = re.json()
        # self.TaskId = re["data"][0]["TaskId"]
        print("======RE输出=======")
        print(re)
        if re["data"] == []:
            print("[OK]没有未完成打卡记录")
            return
        else:
            for x in re["data"]:
                if x["Title"] == "每日健康签到" and x["TimeoutState"] == 1:
                    print("--\n", x["TaskId"])
                    # self.TaskId = re["data"][0]["TaskId"]
                    self.TaskId = x["TaskId"]
                    print("================Get-TaskId================")
                    print("任务id:" + self.TaskId)
                    print("================提交打卡================")
                    self.submit(add, addr, str(self.TaskId))
                    break
                else:
                    print("没有未完成的健康打卡")
            pass
        pass

    # 显示打卡结果
    def show(self, id):
        url = "https://api.uyiban.com/workFlow/c/work/share?InitiateId=" + str(id) + "&CSRF=" + self.CSRF
        cookies = {
            "csrf_token": self.CSRF,
            "PHPSESSID": self.PHPSESSID,
            "cip": self.cpi
        }
        headers = {
            "Origin": "https://app.uyiban.com",
            "User-Agent": "yiban_android"
        }
        re = requests.get(url=url, headers=headers, cookies=cookies)
        try:
            if re is not None:
                print("================审批表================")
                print(re.json()["data"]["uri"])
                return re.json()["data"]["uri"]
        except:
            return None

    # 提交打卡
    def submit(self, add, addr, taskId):
        url = "https://api.uyiban.com/workFlow/c/my/apply/00b3386b830aee855e6f3e6d971578fe?CSRF=" + self.CSRF
        # print(url)
        state = {
            "88424bca49322baa29312b86c48d7c77": ["健康"],
            "eed384ea95c24c499f98c14b9133bf6a": "正常（37.3℃以下）",
            "a04c0ad8bc33167b8ef17eab5fdcc6c3": "无",
            "e340e17239becdb66f7b078e3aedcb04": "是",
            # "c3cda6d6eca68ddec53ddd4dd3258fff": addr
            "3dc4ae0466683f2d7dea16160d956721": add,
            "36b6c0c2edf6980c0231c9714c6106ea": addr
        }
        state = json.dumps(state, ensure_ascii=False)
        extend = {
            "TaskId": taskId,
            "title": "任务信息",
            "content": [
                {
                    "label": "任务名称",
                    "value": "每日健康签到"
                },
                {
                    "label": "发布机构",
                    "value": "学生工作处（部）、武装部"
                }
            ]
        }
        extend = json.dumps(extend, ensure_ascii=False)
        params = {
            "data": state,
            "extend": extend
        }

        cookies = {
            "csrf_token": self.CSRF,
            "PHPSESSID": self.PHPSESSID,
            "cip": self.cpi
        }
        headers = {
            "Origin": "https://app.uyiban.com",
            "User-Agent": "yiban_android"
        }
        # print(type(params))
        # print(params)
        re = requests.post(url=url, data=params, timeout=100, headers=headers, cookies=cookies)
        # print(re.json())
        print("======OK=====")
        '''
        签到成功后re["data"] 可以用作截图界面，，，
        '''
        resultId = re.json()["data"]
        resultUrl = self.show(resultId)
        print("微信推送")
        if self.uid != '123':
            MessageTest.SendMessWxPost(self.uid, resultUrl)
