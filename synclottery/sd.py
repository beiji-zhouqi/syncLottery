#!/usr/bin/env python
# encoding: utf-8

import re
import time
import datetime
from synclottery.requestData import GetData


'''
url: 使用的是360彩票官网接口数据，修改startTime和endTime获取期间数据
sd_re: 获取数据正则表达式
'''

def runSql(start_Time, end_Time):
    url = "https://chart.cp.360.cn/kaijiang/sd?lotId=210053&spanType=2&span=" + start_Time + "_" + end_Time
    sdRe = re.compile(r'<tr week=.*?<td>(.*?)</td><td>(.*?)</td>.*?<span .*?>(.*?)</span>.*?<span .*?>(.*?)</span>.*?<span .*?>(.*?)</span>.*?<td>(.*?)</td>.*?</tr>')
    instance = GetData(url, sdRe)
    data = instance.requestData()
    for i in reversed(data):
        period = i[0]
        r = i[1][:10]
        dataPeriod = i[1][:10]
        testhaoma = i[5][:3]
        haoma = i[2] + i[3] + i[4]
        a = i[2]
        b = i[3]
        c = i[4]
        ab = i[2] + i[3]
        ac = i[2] + i[4]
        bc = i[3] + i[4]
        insertData = (str(period),str(dataPeriod),str(testhaoma),str(haoma),str(a),str(b),str(c),str(ab),str(ac),str(bc))
        sql = "insert into sdhaoma(period,data_period,testhaoma,haoma,a,b,c,ab,ac,bc)values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')"% insertData

        instance.sqlExecute(sql, "insert")

def getYesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    return yesterday

def getTomorrow():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    tomorrow = today + oneday
    return tomorrow

def sdRun():
    instance = GetData('', '')
    select_result = instance.sqlExecute("select data_period from sdhaoma order by data_period  desc limit 1", "select")
    timeArray = time.localtime(int(time.time()))
    endTime = time.strftime("%Y-%m-%d",timeArray)
    if len(select_result) == 0:
        startTime = "2017-01-01"
        runSql(startTime, endTime)
    elif select_result[0][0] == getYesterday() and int(time.time()) > 79200:
        runSql(getTomorrow(), endTime)
    elif select_result[0][0] != getYesterday():
        startTime = select_result[0][0]
        runSql(startTime, endTime)
    else:
        print('no run_sql')

