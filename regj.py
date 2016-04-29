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
import pytz
from xml.dom import minidom
domains = ["rimsschool.in", "jainhospital.in"] 
st = datetime.datetime.strptime("2016-04-28 04:00:00", "%Y-%m-%d %H:%M:%S")
tz = pytz.timezone('Asia/Shanghai') 
st = tz.localize(st)
class regThread(threading.Thread):
    def __init__(self, domain):
        threading.Thread.__init__(self)
        self.domain = domain

    def run(self):
        
        def reg():
            regurl = "https://test.httpapi.com/api/domains/register.xml?auth-userid=646057&api-key=VN4E2vJMgCYMUFug7mIg4MVZ7yGkUwRT&domain-name=" + self.domain + "&years=1&ns=ns1.domain.com&ns=ns2.domain.com&customer-id=14672593&reg-contact-id=53657111&admin-contact-id=53657111&tech-contact-id=53657111&billing-contact-id=53657111&invoice-option=PayInvoice"
    
            i = 1
            t1 = datetime.datetime.now(tz)
            print(self.domain, "now:", t1, "start request")
            while 1 :
                
              
                    
                req = requests.get(regurl,timeout=5)
    
                print(req.text)
                if(checksuccess(req.text)):
                    print(self.domain, "sale sucessful")
                    break
    
                
                    
                t2 = datetime.datetime.now(tz)
                print(self.domain, "register time", t2, "requests", i, "times")
                tm = (t2 - t1).seconds / (60)
    
                if(i >= 200) :
                    break
                i = i + 1    
                if(tm >= 0 and tm < 1):
                    time.sleep(10)
                elif(tm >= 1 and tm < 2.5):
                    time.sleep(1)
                elif(tm >= 2.5 and tm < 3):
                    time.sleep(10)    
                elif(tm >= 3 and tm < 5):
                    time.sleep(5)    
                elif(tm >= 5 and tm < 6):
                    time.sleep(1)
                elif(tm >= 6 and tm < 10):
                    time.sleep(30)
                elif(tm >= 10 and tm < 50):
                    time.sleep(180)    
                else:
                    break        


        def checksuccess(xml):
            
            doc = minidom.parseString(xml)


            root = doc.documentElement


            entrys = root.getElementsByTagName("entry")

            for entry in entrys:


                sta = entry.getElementsByTagName("string")[0].childNodes[0].nodeValue.lower()
                suc = entry.getElementsByTagName("string")[1].childNodes[0].nodeValue.lower()
                print(sta,suc)
                if(sta == "status" and suc == "success"):

                    return True

            return False
        reg()
        try :
            print("close programe")
            os._exit(0)
        except:
            print("close fail")



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

    for i in domains:
        t = regThread(i)
        t.start()
















