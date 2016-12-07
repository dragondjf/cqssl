#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime
from peewee import *
from log import logger

# db = MySQLDatabase('Cqssc', user="root", passwd="djf", threadlocals=True)
# db.execute_sql('''
#     DROP DATABASE IF EXISTS `Cqssc`;
#     CREATE DATABASE `Cqssc` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;
#     ''')

db = SqliteDatabase("app/cqssc.db", threadlocals=True)



class BaseModel(Model):
    class Meta:
        database = db

    @classmethod
    @db.atomic()
    def getRecord(cls,  **kwargs):
        key = getattr(cls, '__key__')
        assert key in kwargs
        try:
            ret = cls.get(getattr(cls, key) == kwargs[key])
            return ret
        except DoesNotExist:
            return None

    @classmethod
    def isRecordExisted(cls, **kwargs):
        ret = cls.getRecord(**kwargs)
        if ret:
            return True
        else:
            return False

    @classmethod
    @db.atomic()
    def updateRecord(cls, **kwargs):
        key = getattr(cls, '__key__')
        assert key in kwargs
        retId = cls.update(**kwargs).where(getattr(cls, key) == kwargs[key]).execute()
        if retId != 0:
            return True
        else:
            return False

    @classmethod
    @db.atomic()
    def createRecord(cls, **kwargs):
        key = getattr(cls, '__key__')
        assert key in kwargs
        try:
            ret = cls.create(**kwargs)
        except IntegrityError:
            ret = None
        return ret

    @classmethod
    def createRecords(cls, records):
        with db.transaction() as txn:
            for record in records:
                try:
                    ret = cls.create(**record)
                except IntegrityError:
                    ret = None

    @classmethod
    @db.atomic()
    def get_create_Record(cls, **kwargs):
        key = getattr(cls, '__key__')
        assert key in kwargs
        try:
            ret = cls.create(**kwargs)
        except IntegrityError:
            # print('%s is already in use' % kwargs['url'])
            retId = cls.update(**kwargs).where(getattr(cls, key) == kwargs[key]).execute()
            if retId != 0:
                ret = cls.get(cls.id==retId)
            else:
                ret = None
        return ret

    @classmethod
    def get_create_Records(cls, records):
        with db.transaction():
            for record in records:
                key = getattr(cls, '__key__')
                assert key in record
                try:
                    ret = cls.create(**record)
                except IntegrityError:
                    cls.update(**record).where(getattr(cls, key) == record[key]).execute()


class Lottery(BaseModel):
    lottery_day = IntegerField()
    lottery_number = BigIntegerField()
    one = IntegerField()
    two = IntegerField()
    three = IntegerField()
    four = IntegerField()
    five = IntegerField()
    sum = IntegerField()
    created_date = DateTimeField(default=datetime.datetime.now)

    __key__ = 'lottery_number'

    def toDict(self):
        keys = ['lottery_day', "lottery_number", "one",
            "two", "three", "four", "five", "sum"
        ]
        ret = {}
        for key in keys:
            ret.update({key: getattr(self, key)})
        return ret

    @classmethod
    def readData(cls, filename):
        with open(filename, "r") as f:
            rawDataLines = f.readlines()
        logger.warning("start read data")
        recordDatas = []
        for line in rawDataLines:
            line = repr(line)
            keyStart = line.find("20")
            keyEnd = line.find("\\t")
            key = line[keyStart:keyEnd]

            valueStart = keyEnd + 2
            valueEnd = -5

            rawData_string = line[valueStart:valueEnd].split(",")

            value = [int(item) for item in 
                line[valueStart:valueEnd].split(",")]

            lottery_day = int(key.replace('-', '')[:-3])
            lottery_number = int(key.replace('-', ''))
            
            recordData = {
                'lottery_day' : lottery_day,
                'lottery_number': lottery_number,
                'one': value[0],
                'two': value[1],
                'three': value[2],
                'four': value[3],
                'five': value[4],
                'sum': sum(value)
            }
            recordDatas.append(recordData)
        logger.warning("Read data finished")
        logger.warning("start write to db")
        Lottery.createRecords(recordDatas)
        logger.warning("write dat to db finished")

    @classmethod
    def getRecordByDay(cls, day):
        rets = []
        for record in Lottery.select().where(Lottery.lottery_day==day):
            rets.append(record)
        return rets


class DBWorker(object):

    def __init__(self):
        super(DBWorker, self).__init__()
        db.connect()

    def loadData(self, filePath):
        tables = [Lottery]
        db.drop_tables(tables, safe=True)
        db.create_tables(tables, safe=True)
        Lottery.readData(filePath)

    def readData(self):
        for lottery in Lottery.select():
            print lottery.lottery_day, lottery.lottery_number

    def test(self):
        print(db.get_tables())
        for r in Lottery.getRecordByDay(20160914):
            print r.one, r.two, r.three, r.four, r.five
        # self.readData()

dbWorker = DBWorker()
