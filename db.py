#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.model import dbWorker, Lottery

def classfiyData(data):
    i = 0
    splitRet = []
    oddRet = {}
    evenRet = {}
    while i < len(data):
        j = i
        odd = []
        even = []
        while True:
            if j < len(data) - 1:
                if  (data[j] + data[j+1]) % 2 == 0:    
                    if data[j] % 2 == 0:
                        even.append(data[j])
                    else:
                        odd.append(data[j])
                else:
                    if data[j] % 2 == 0:
                        even.append(data[j])
                    else:
                        odd.append(data[j])
                    break
                j = j + 1
            else:
                if data[j] % 2 == 0:
                    even.append(data[j])
                else:
                    odd.append(data[j])
                break
        if len(odd) > 0:
            splitRet.append(odd)
        if len(even) > 0:
            splitRet.append(even)

        if len(even) >=1:
            i = i + len(even)
        elif len(odd) >= 1:
            i = i + len(odd)
        else:
            i = i + 1

    count = 0
    for r in splitRet:
        if r[0] % 2 == 0:
            if len(r) not in evenRet:
                evenRet[len(r)] = 1
            else:
                evenRet[len(r)] = evenRet[len(r)] + 1
        else:
            if len(r) not in oddRet:
                oddRet[len(r)] = 1
            else:
                oddRet[len(r)] = oddRet[len(r)] + 1
        count += len(r)
    return oddRet, evenRet, splitRet


def analyzeOneDay(date, dataType="one"):
    data = [record[dataType] for record in  Lottery.getRecordByDay(date)]
    oddRet, evenRet, splitRet = classfiyData(data)
    return oddRet, evenRet, splitRet, data
    


ret = {}
retSet = {}
retCounts = {}
for dataType in ['one', 'two', 'three', 'four', 'five']:
    ret[dataType] = []
    for month in range(1, 13):
        if month < 10:
            date_month = "2013" + "0" + str(month)
        else:
            date_month = "2013" + str(month)
        for day in range(1, 32):
            if day < 10:
                date = date_month + "0" + str(day)
            else:
                date = date_month + str(day)
            oddRet, evenRet, splitRet, data= analyzeOneDay(date, dataType)
            if oddRet and evenRet:
                maxCount = max([max(oddRet.keys()), max(evenRet.keys())])
                ret[dataType].append(maxCount)
            else:
                print date
    retSet[dataType] = set(ret[dataType])
    retCounts[dataType] = {}
    for v in retSet[dataType]:
        retCounts[dataType].update({v: ret[dataType].count(v)})

print ret
print retSet
print retCounts
for k, v in  ret.items():
    print k, len(v)
for k, v in  retCounts.items():
    print k, sum(v.values())
# analyzeOneDay(20141124)


# day = 20150101
# i = 0
# while i < 30:
#     day += 1
#     ones = [record['one'] for record in  Lottery.getRecordByDay(day)]
#     print day, len(ones), ":"
#     classfiyData(ones)
#     i += 1
