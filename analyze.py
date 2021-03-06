#!/usr/bin/env python
# -*- coding: utf-8 -*-

from log import logger
import collections
import datetime
from app.model import dbWorker, Lottery


class AnalyzeTool(object):

    def __init__(self):
        super(AnalyzeTool, self).__init__()

    @classmethod
    def small(self, data, number=3):
        datas = collections.OrderedDict()
        for i in range(len(data) - number):
            _smallData = []
            spliceData = data[i: number + i]

            for x in spliceData:
                if x < 5:
                    _smallData.append(x)
                else:
                    break
            if _smallData == spliceData:
                if (data[i - 1] >= 5) and (data[number + i] >= 5):
                    datas[i] = spliceData
        return datas


class DayModel(object):
    
    keys = ['one', 'two', 'three', 'four', 'five', "sum"]

    def __init__(self, day):
        super(DayModel, self).__init__()
        self.day = day
        for key in self.keys:
            setattr(self, key, [])
        for key in self.keys:
            setattr(self, key + "result", {})
        self.result = {}
        self.udpate()
        self.computer()


    def udpate(self):
        data = {}
        for key in self.keys:
            data[key] = []
        for r in Lottery.getRecordByDay(self.day):
            for key in self.keys:
                data[key].append(getattr(r, key))
        for key in self.keys:
            data[key].reverse()
            setattr(self, key, data[key])

    def computer(self):
        for key in self.keys[0:-1]:
            for x in xrange(1, 30):
                datas = AnalyzeTool.small(getattr(self, key), x)
                if len(datas) > 0:
                    # print key , x, len(datas)
                    getattr(self, key + "result")[x] = len(datas)

    def printResult(self, start=4, end=11):
        count = 0
        m = 0
        for key in self.keys[0:-1]:
            # print getattr(self, key)
            ret = getattr(self, key + "result")
            # print key, ret
            count += sum(ret.values())

            lost = 0
            for x in range(0, end - start + 1):
                lost += 10* pow(2, x)

            # print lost
            for key in ret.keys():
                if key < start:
                    continue
                if key <= end:
                    m += ret[key]*10 * 0.95
                else:
                    m -= lost * ret[key]

        return count, m


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date+datetime.timedelta(n)
  


def main():
    # dbWorker.loadData("app/cqssc.txt")

    begin = datetime.datetime(2016, 1, 1)
    end = datetime.datetime(2016, 8, 31)

    for t in range(17, 30):
        money = []
        for i in date_range(begin, end):
            day = int(i.strftime('%Y%m%d'))
            # print "============" + str(day) + "================"
            dayModel = DayModel(day)
            ret, m = dayModel.printResult(17, t)
            money.append(m)
            # print "============" + str(ret) + "  " + str(m) + "================"
        print "***************" + str(t) + "   " + str(sum(money)) + "************************"



if __name__ == '__main__':
    main()
