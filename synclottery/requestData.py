#!/usr/bin/env python
# encoding: utf-8

import requests
import re
import yaml
import os
import pymysql

'''
    url和re正则的写法
    :params
    url = "https://chart.cp.360.cn/kaijiang/sd?lotId=210053&spanType=2&span=2017-01-01_2019-12-01"
    caipiao_re = re.compile(r'<tr week=.*?<td>(.*?)</td><td>(.*?)</td>.*?<span .*?>(.*?)</span>.*?<span .*?>(.*?)</span>.*?<span .*?>(.*?)</span>.*?</tr>')
'''

class GetData:
    def __init__(self, url, caiPiaoRe):
        self.url = url
        self.caiPiaoRe = caiPiaoRe

    def requestData(self):
        req = requests.get(self.url, timeout=10)
        try:
            if req.status_code == 200:
                msg = req.content
                html = msg.decode('utf-8', 'ignore')
                dataList = self.caiPiaoRe.findall(html)
                return dataList
            else:
                print("error")
        except Exception as e:
            print("error:", e)

    def getConfig(self):
        try:
            f = open(os.path.join(os.path.dirname(__file__), '../config/config.yml'), 'r', encoding='utf-8')
            return yaml.load(f.read())
        except Exception as e:
            print("error:",e)

    def sqlExecute(self, sql, tag):
        configData = self.getConfig()
        db = pymysql.connect(host=configData['DB']['host'],
                            user=configData['DB']['username'],
                            password=configData['DB']['password'],
                            database=configData['DB']['database'],
                            port=configData['DB']['port'],
                            charset="utf8")    
        cursor = db.cursor()
        if tag == "select" or tag == "SELECT":
            try:
                cursor.execute(sql)
                results = cursor.fetchall()
                return results
            except Exception as e:
                print("error:", e)
        elif tag == "insert" or tag == "INSERT":
            try:
                cursor.execute(sql)
                db.commit()
            except Exception as e:
                db.rollback()
                print("error:", e)
                print("error sql:",sql)
        else:
            print("----------------------")
            pass
        db.close()
