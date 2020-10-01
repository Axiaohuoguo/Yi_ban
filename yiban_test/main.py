import json
import signin
if __name__ == '__main__':
    signin = signin.Signin("","")
    data = open("studentinfo.json",encoding="UTF-8")
    strJson = json.load(data)
    i = 0
    j = 0
    for x in strJson:
        i = i + 1
    while j < i:
        j = j + 1
        user=strJson[str(j)]["user"]
        pasw=strJson[str(j)]["pasw"]
        addr = strJson[str(j)]["addr"]
        add = strJson[str(j)]["add"]
        signin.account = user
        signin.passwd = pasw
        signin.login()
        signin.getLocation()
        signin.getuncompletedList(addr,add)
        # signin.show("7fe1cdb05a5a213e92acd52a2575d18b")
    data.close()


