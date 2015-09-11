#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.httpclient
from pyquery import PyQuery as pq
from .websockerhandler import WebSocketManagerHandler
from .analyze import CodeManager


class PeriodicTask(object):

    interval = 5000

    def __init__(self, *args, **kwargs):
        super(PeriodicTask, self).__init__()
        self.timer = tornado.ioloop.PeriodicCallback(
            self.fetchData, self.interval)
        self.http_client = tornado.httpclient.AsyncHTTPClient()

        self.codeManager = CodeManager()

    def fetchData(self):
        self.http_client.fetch(
            "http://yhw002.com/app/member/Lottery/list.php?t=1",
            self.handle_request)

    def handle_request(self, response):
        if response.error:
            print "Error:", response.error
        else:
            html = response.body
            html = html.replace("images/", "static/images/")
            start = html.find("<body>") + len("<body>")
            end = html.find("</body>")
            result = self.codeManager.initCodeObjsByHtml(html)
            WebSocketManagerHandler.send_updates({
                "data": html[start:end],
                "result": result
            })

    def start(self):
        self.fetchData()
        self.timer.start()

    def stop(self):
        self.timer.stop()

    def is_running(self):
        return self.timer.is_running()

task = PeriodicTask()
