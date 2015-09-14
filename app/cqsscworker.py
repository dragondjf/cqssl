#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from collections import OrderedDict
from signalmanager import signalManager


class CqsscWorker(QObject):

    def __init__(self, parent=None):
        super(CqsscWorker, self).__init__(parent)
        self._rawDataLines = []
        self._rawData = OrderedDict()
        self._rawData_number = OrderedDict()
        self._rawData_ballone = OrderedDict()
        self._rawData_balltwo = OrderedDict()
        self._rawData_ballthree = OrderedDict()
        self._rawData_ballfour = OrderedDict()
        self._rawData_ballfive = OrderedDict()
        self._rawData_sumsize = OrderedDict()
        self._rawData_sumparity = OrderedDict()

    def analyzeData(self, filename="cqssc_data.txt"):
        signalManager.statusTextChanged.emit("reading data")
        self.readData(filename)

        values = self._rawData_number.values()
        print len(values), len(set(values)), len(values) - len(set(values))

        result = CqsscWorker.searchPattern(self._rawData_sumsize.values(), mode=0, count=13)
        print result

    def readData(self, filename):
        with open(filename, "r") as f:
            self._rawDataLines = f.readlines()
        # print self._rawDataLines[0:100]
        for line in self._rawDataLines[0:200]:
            line = repr(line)
            keyStart = line.find("20")
            keyEnd = line.find("\\t")
            key = line[keyStart:keyEnd]

            valueStart = keyEnd + 2
            valueEnd = -5

            rawData_string = line[valueStart:valueEnd].split(",")

            value = [int(item) for item in 
                line[valueStart:valueEnd].split(",")]
            self._rawData.update({key: value})
            self._rawData_number.update({key: int("".join(rawData_string))})
            self._rawData_ballone.update({key: value[0]})
            self._rawData_balltwo.update({key: value[1]})
            self._rawData_ballthree.update({key: value[2]})
            self._rawData_ballfour.update({key: value[3]})
            self._rawData_ballfive.update({key: value[4]})

            if sum(value) >= 23:
                self._rawData_sumsize.update({key: 1})
            else:
                self._rawData_sumsize.update({key: 0})

            if sum(value) % 2 == 0:
                self._rawData_sumparity.update({key: 1})
            else:
                self._rawData_sumparity.update({key: 0})
            if key <= "20150913-101":
                print self._rawData_sumsize[key], value, sum(value)
        signalManager.statusTextChanged.emit("reading data finished")

    @staticmethod
    def searchPattern(source, mode=0,count=4):
        pattern = []
        pattern.append(1-mode)
        for i in range(count):
            pattern.append(mode)
        pattern.append(1-mode)

        print pattern, source
        result = []
        for start in range(len(source)):
            end = start + len(pattern)
            if source[start:end] == pattern:
                result.append(start)
        return result
