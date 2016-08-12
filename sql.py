import pymysql
import time
import pytz
import datetime

tz = pytz.timezone('Asia/Shanghai')
domains=[]

def getDomains():
    strday=datetime.datetime.now(tz).strftime('%Y-%m-%d')
    conn=pymysql.connect(host='127.0.0.1',user='root',passwd='wb123456',db='name',port=3306)
    cur=conn.cursor()
    sql='select domain from domain where date="'+strday+'"'
    cur.execute(sql)
    
    for i in cur.fetchall():
        for j in i:
            domains.append(j)
    conn.close()
    return domains

if __name__=="__main__":
    # print(strday)
    print(getDomains())