'''
Created on 2016-08-07

@author: wubiao
'''
#coding=utf-8

import requests
import time
import threading
import datetime
import pytz
# import json
import sys
from tldextract import extract
import sql
import hashlib
import urllib.parse
from xml.dom import minidom

stime = "12:30:00"
etime = "23:50:00"


tz = pytz.timezone('Asia/Shanghai')

class Login:
    sys_api = "http://api.west263.com/api/"
    sys_user= "domainindia"
    sys_pass= "wb123456"

    def __init__(self):
        pass

class API(Login):


    def __init__(self):

        pass


    def check(self, domain):
        subdomain, maindomain, tld = extract(domain)

        cmdstrng ="domainname"+"\r\n"+"check"+"\r\n"+"entityname:domain-check"+"\r\n"+"domainname:"+maindomain+"\r\n"+"suffix:."+tld+"\r\n"+"."+"\r\n"
        cmdstrng=urllib.parse.quote_plus(cmdstrng)
        md5sing=hashlib.md5((self.sys_user+self.sys_pass+cmdstrng[0:10]).encode()).hexdigest()
        postdata=self.sys_api+"?userid="+self.sys_user+"&versig="+md5sing+"&strCmd="+cmdstrng
        try:
            res = requests.get(postdata,timeout=30)
            print(res.text)
            doc = minidom.parseString(res.text)
            root = doc.documentElement
            allow = root.getElementsByTagName("allow")[0].childNodes[0].nodeValue.lower()
            print(allow)
        except:
            print(domain+" check except")
            return "except"
        if(allow==domain):
            print(domain + " check success")
            return "suc"
        else:
            print(domain + " check fail")
            return "fail"


    def reg(self, domain):

        cmdstrng ="domainname"+"\r\n"+"add"+"\r\n"+"entityname:domain"+"\r\n"+"domainname:"+domain+"\r\n"+"term:1"+"\r\n"+"dom_org:zhang xiaoguang"+"\r\n"+"dom_fn:xiao guang"+"\r\n"+"dom_ln:zhang"+"\r\n"+"dom_adr1:Huan Qiu Guang Chang 24Lou 2Hao"+"\r\n"+ "dom_ct:cheng du"+"\r\n"+"dom_st:SC"+"\r\n"+"dom_co:cn"+"\r\n"+"dom_pc:610001"+"\r\n"+"dom_ph:028-87654321"+"\r\n"+"dom_fax:028-87654321"+"\r\n"+"dom_em:axhar15809@163.com"+"\r\n"+"dom_org_m:wangke"+"\r\n"+"dom_fn_m:wangke"+"\r\n"+"dom_ln_m:wang"+"\r\n"+"dom_adr_m:hefeishijinganqu"+"\r\n"+"dom_ct_m:hefei"+"\r\n"+"dom_st_m:anhui"+"\r\n"+"domainpwd:jtc11v"+"\r\n"+"ppricetemp:30"+"\r\n"+"."+"\r\n"
        md5sing=hashlib.md5((self.sys_user+self.sys_pass+cmdstrng[0:10]).encode()).hexdigest()
        postdata=self.sys_api+"?userid="+self.sys_user+"&versig="+md5sing+"&strCmd="+cmdstrng
        # print(postdata)
        try:
            res = requests.get(postdata,timeout=30)
            print(res.text)
            doc = minidom.parseString(res.text)
            root = doc.documentElement

            returncode = root.getElementsByTagName("returncode")[0].childNodes[0].nodeValue.lower()
        except:
            time.sleep(0.5)
            return "except"
        if(returncode == "200"):
            return "suc"
        else:
            return "fail"

class regThread(threading.Thread):
    def __init__(self, domain):
        threading.Thread.__init__(self)
        self.domain = domain

    def run(self):

        def doreg():
            api = API()
#             api.username = username
#             api.api_token = api_token
            # api.login()
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
                    api.reg(self.domain)
                    print("request sale ",self.domain," success ")

                    break


                t2 = datetime.datetime.now(tz)
                print(self.domain, "register time", t2, "requests", i, "times")
                # tm = (t2 - t1).seconds / (60)
                tm = (t2 - t1).seconds /(60)


                if(t2 >= et):
                    break

                if(i >= 100) :

                    break

                i = i + 1

                if(tm >= 0 and tm < 10):
                    time.sleep(60)
                elif(tm >= 10 and tm < 30):
                    time.sleep(3*60)

                elif(tm >= 30 and tm < 40):
                    time.sleep(60)
                elif(tm >= 40 and tm < 60):
                    time.sleep(3*60)
                elif(tm >= 60 ):
                    time.sleep(5*60)
                else:
                    break
            print(self.domain,"break while loop")
            time.sleep(tms)
            print(self.domain,"thread over")
        doreg()



def checktime():

    while 1 :


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





























