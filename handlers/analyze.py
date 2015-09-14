#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyquery import PyQuery as pq


def getSameItem(items):
    sset = None
    if len(set(items)) == 1:
        return items
    else:
        for i in xrange(len(items)):
            _citems = items[0:(i+1)]
            if len(_citems) >= 2:
                sset = set(_citems)
                if (len(sset) == 1):
                    continue
                else:
                    break
        return _citems[0:i]


class CodeObj(object):
    
    def __init__(self, *args, **kwargs):
        super(CodeObj, self).__init__()
        self._code = None
        self._size = None
        self._sum = None
        self._parity = None
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    @property
    def sum(self):
        return self._sum

    @sum.setter
    def sum(self, value):
        self._sum = value

    @property
    def parity(self):
        return self._parity

    @parity.setter
    def parity(self, value):
        self._parity = value

    

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)


class CodeManager(object):
    def __init__(self):
        super(CodeManager, self).__init__()
        self._codeObjs = []
        # self.initCodeObjsByHtml(html)

    def initCodeObjsByHtml(self, html):
        self._codeObjs = []
        d = pq(html)
        for item in d("td.img"):
            _code = []
            _size = None
            _sum = None
            
            _parity = None
            for item in d(item)("img"):
                _code.append(int(d(item).attr("src")[-5]))

            _size  = sum(_code)

            if _size >= 23:
                _sum = "large"
            else:
                _sum = "small"

            if _size % 2 == 0:
                _parity = "even"
            else:
                _parity = "odd"

            _item = {
                "code": _code,
                "size": _size,
                "sum": _sum,
                "parity": _parity
            }
            obj = CodeObj(**_item)
            self._codeObjs.append(obj)

        return self.analyzeData()

    @property
    def codeObjs(self):
        return self._codeObjs

    def analyzeData(self):
        objs = self._codeObjs[:-10]
        sums = [obj.sum for obj in objs]
        paritys = [obj.parity for obj in objs]
        sumsResult =  getSameItem(sums)
        paritysResult =  getSameItem(paritys)

        result = {
            "large": 0,
            "small": 0,
            "odd": 0,
            "even": 0,
        }
        if 'small' in sumsResult:
            result['small'] = len(sumsResult)
        if 'large' in sumsResult:
            result['large']  = len(sumsResult)
        if 'odd' in paritysResult:
            result['odd']  = len(paritysResult)
        if 'even' in paritysResult:
            result['even']  = len(paritysResult)

        return result
