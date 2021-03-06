'''
Created on 2016-08-07

@author: wubiao
'''

import requests
import time
import threading
import datetime
import pytz
import json
import sys
from tldextract import extract
import sql



stime = "03:59:00"
etime = "04:05:00"


tz = pytz.timezone('Asia/Shanghai')
# strday=datetime.datetime.now(tz).strftime('%Y-%m-%d')
# 使用API登录name
class Login:
    username = 'wubiao239'
    api_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcGl0IjoxMjg2ODYyLCJleHAiOjE3ODU4NTc1NDQsImp0aSI6MX0.0LxzVX1mUa9Tg6i296mk80RtO047jaL6mgRyV9316bY'

    session_token = ""

    def __init__(self):
        pass

    def login(self):
        param = {'username':self.username, 'api_token':self.api_token}
        res = requests.session().post("https://api.name.com/api/login", data=json.dumps(param), timeout=10)
        # res=requests.get("https://api.dev.name.com/api/account/get");

        self.session_token = json.loads(res.text)['session_token']
        print(res.text)

class API(Login):
    # username='wubiao239-ote';
    # api_token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcGl0Ijo1NjE4NjgsImV4cCI6MTc4NTg1NzUzNiwianRpIjoxfQ.bMwNLDloRoOuhYPGvpGwl3dIYPkokIzU_FZrMgEmIL8';

    nameservers = ['ns1.name.com', 'ns2.name.com', 'ns3.name.com', 'ns4.name.com']
    contacts = [{'type': ['registrant', 'administrative', 'technical', 'billing'],
            'first_name': 'njl',
            'last_name': 'nvp',
            'organization': 'Name.com',
            'address_1': '100 Main St.',
            'address_2': 'Suite 300',
            'city': 'Denver',
            'state': 'CO',
            'zip': '80230',
            'country': 'US',
            'phone': '+1.3035555555',
            'fax': '+1.3035555556',
            'email': 'njlnvp26022@163.com',
            }]

    def __init__(self):

        pass

    # res=requests.session().get("https://api.name.com/api//account/get ",headers=headers)
    # 
    # 使用API注册域名
    def check(self, domain):
        subdomain, maindomain, tld = extract(domain)
        param = {"keyword":maindomain, "tlds":[tld], "services":["availability"]}
        headers = {'Api-Username':self.username, 'Api-Token':self.api_token, 'Api-Session-Token':self.session_token}
        res = requests.session().post("https://api.name.com/api/domain/check", data=json.dumps(param), headers=headers, timeout=10)
        print(res.text)
        try:
            result = json.loads(res.text)['domains'][domain]['avail']
            print(result)
        except:
            print("tlds not find")
            return "null";
        
        if(result):
            print(domain + " check success")
            return "suc"
        else:
            print(domain + " check fail")
            return "fail"

    # 使用API注册域名
    def reg(self, domain):
        param = {'domain_name' : domain,
                'period' : 1 ,
                'nameservers': self.nameservers,
                'contacts': self.contacts,
                }
        headers = {'Api-Username':self.username, 'Api-Token':self.api_token, 'Api-Session-Token':self.session_token}
        for i in range(1,3):
            try:
                res = requests.session().post("https://api.name.com/api/domain/create", data=json.dumps(param), headers=headers, timeout=10)
                print(res.text)
                code = json.loads(res.text)['result']['code']
                print(code)
            except:
                
                print(self.domain," sale success")
                break
        
# 使用多线程注册
class regThread(threading.Thread):
    def __init__(self, domain):
        threading.Thread.__init__(self)
        self.domain = domain

    def run(self):

        def doreg():
            api = API()
#             api.username = username
#             api.api_token = api_token
            api.login()
            i = 1
            t1 = datetime.datetime.now(tz)
            strday = datetime.datetime.now(tz).strftime('%Y-%m-%d')
            et = datetime.datetime.strptime(strday + " " + etime, "%Y-%m-%d %H:%M:%S")
            et = tz.localize(et)
            st = datetime.datetime.strptime(strday + " " + stime, "%Y-%m-%d %H:%M:%S")
            st = tz.localize(st)
            tms = (et - st).seconds
            print(self.domain, "now:", t1, "start request")
            while 1 :

                req = api.check(self.domain)
                
                print(req)
                
                if(req=="suc"):
                    break
                    
                if(req=="null"):
                    break
                t2 = datetime.datetime.now(tz)
                print(self.domain, "register time", t2, "requests", i, "times")
                tm = (t2 - t1).seconds / (60)
                
                # 控制时间当到结束时间时跳出循环
                if(t2 >= et):
                    break
                # 控制请求次数，当请求次数大于200次时跳出循环
                if(i >= 200) :
                    
                    break
                
                i = i + 1
                # 控制请求次数，十分钟内不同时间请求次数快慢变化
                if(tm >= 0 and tm < 1):
                    time.sleep(3)
                elif(tm >= 1 and tm < 3):
                    time.sleep(0.8)

                elif(tm >= 3 and tm < 5):
                    time.sleep(1)
                elif(tm >= 5 and tm < 6):
                    time.sleep(3)
                elif(tm >= 6 and tm < 10):
                    time.sleep(5)
                else:
                    break
            print(self.domain,"break while loop")    
            if(req=="suc"):
                         
                res = api.reg(self.domain)
                    
            
            time.sleep(tms)
            print(self.domain,"thread over")
        doreg()



def checktime():

    while 1 :

        # 将字符转换为上海的当天时间
        strday = datetime.datetime.now(tz).strftime('%Y-%m-%d')

        st = datetime.datetime.strptime(strday + " " + stime, "%Y-%m-%d %H:%M:%S")
        et = datetime.datetime.strptime(strday + " " + etime, "%Y-%m-%d %H:%M:%S")
        st = tz.localize(st)
        et = tz.localize(et)
        # print(st)
        # print(et)
        # domains = []
        now = datetime.datetime.now(tz)

        if now >= st and now <= et:
            domains=sql.getDomains()
            print(domains)
            if(len(domains) >= 1):
                print("regist now:", now)
                regDomains(domains)
            else:
                print("no domains register")

        else:
            print("time:", now, "try it later")
        time.sleep(60)
    print ("multi thread to regist")

# 启动多线程
def regDomains(domains):
    threads = []
    for i in domains:
        threads.append(regThread(i))
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':

    checktime()





























