'''
Created on 2016-4-11

@author: wubiao
'''


__author__ = 'wubiao'


import requests
import time
import threading
import datetime
import os
import  json
from tldextract import extract
import pytz
from xml.dom import minidom
import random

#domain<=5
###config
domains = ["collegesphere.co.in","theganchimuslimhospital.in","edusocial.in"] 
customerid="14663552"
contactid="53312520"
starttime="2016-04-24 04:00:00"
###config

st = datetime.datetime.strptime(starttime, "%Y-%m-%d %H:%M:%S")
tz = pytz.timezone('Asia/Shanghai') 
st = tz.localize(st)
class regThread(threading.Thread):
    def __init__(self, domain):
        threading.Thread.__init__(self)
        self.domain = domain

    def run(self):
        subdomain, maindomain, tld = extract(self.domain)

        regurl = "https://test.httpapi.com/api/domains/register.xml?auth-userid=646061&api-key=sP6NPKSyagaoitKcihSlMMdAEmot3zFq&domain-name=" + self.domain + "&years=1&ns=ns1.domain.com&ns=ns2.domain.com&customer-id="+ customerid +"&reg-contact-id="+contactid+"&admin-contact-id="+contactid+"&tech-contact-id="+contactid+"&billing-contact-id="+contactid+"&invoice-option=PayInvoice"


        def reg():
            j = 1
            while 1 :
                try :


                    r = requests.get(regurl)
                    print(self.domain,"try register",j,"times")
                    if(checksuccess(r.text)):
                        print(self.domain, "sale sucessful")
                        break


                except Exception:

                    print("request except try again!")
                j = j + 1
                if(j >= 3):
                    break

        def checksuccess(xml):
            doc = minidom.parseString(xml)


            root = doc.documentElement


            entrys = root.getElementsByTagName("entry")

            for entry in entrys:


                sta = entry.getElementsByTagName("string")[0].childNodes[0].nodeValue.lower()
                suc = entry.getElementsByTagName("string")[1].childNodes[0].nodeValue.lower()
                #print(sta,suc)
                if(sta == "status" and suc == "success"):

                    return True

            return False



        reg()

        try :
            print("close programe")
            os._exit(0)
        except:
            print("close fail")

def register(domains):


    i = 1
    j=1
    t1 = datetime.datetime.now(tz)
    while 1 :
        strdomains=""
        strtlds=""
        for domain in domains:
              
            subdomain, maindomain, tld = extract(domain)
            strdomains =strdomains+"&domain-name="+maindomain
            strtlds=strtlds+ "&tlds=" +tld
        checkurl = "https://test.httpapi.com/api/domains/available.json?auth-userid=646061&api-key=sP6NPKSyagaoitKcihSlMMdAEmot3zFq" + strdomains + strtlds  
        try :
            r = requests.get(checkurl,timeout=10)
            j=j+1

            print(datetime.datetime.now(tz), "alread check", j, "times")

        except:
            print("request excption")
            
        for domain in domains:
            
            res = json.loads(r.content.decode())
            # print(res)
            
            status = res.get(domain).get('status')
            
            print(domain, status)
            if status and status.lower == 'unknown':
                t = regThread(domain)
                t.start()

            if status and status.lower() == 'available':
                print("available", domain)
                t = regThread(domain)
                t.start()
                domains.remove(domain)
                
               
            

        time.sleep(2)
        if(len(domains)==0):
            break
        t2 = datetime.datetime.now(tz)
        #if(i % 50 == 0):
            #print(self.domain, "alread check", i , "times")

        tm = (t2 - t1).seconds / (60)

        if(tm >= 8) :
            #t=random.randint(1,10)
            time.sleep(10)
            if(tm>=40):
                break
        i = i + 1   

def checktime():
    print("regist time:", st)
    while 1 :
        now = datetime.datetime.now(tz)

        if now >= st:
            print("regist now:", now)
            break
        else:
            print("time:", now, "try it later")
        time.sleep(60)
    print ("multi thread to regist")

if __name__ == '__main__':

    checktime()
    register(domains)
    #regThread("ampac.in").start()















