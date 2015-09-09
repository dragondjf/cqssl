#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import tornado.websocket
import tornado.escape


class WebSocketManagerHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    cache = []
    cache_size = 200

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    @classmethod
    def update_cache(cls, chat):
        cls.cache.append(chat)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size:]

    @classmethod
    def send_updates(cls, chat):
        logging.info("sending message to %d waiters", len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except:
                logging.error("Error sending message", exc_info=True)

    def open(self):
        logging.info("waiter id: %d opened" % id(self))
        self.waiters.add(self)

    def on_close(self):
        logging.info("waiter id: %d closed" % id(self))
        self.waiters.remove(self)

    def on_message(self, message):
        logging.info("got message %s", message)
        try:
            obj = tornado.escape.json_decode(message)
            self.update_cache(obj)
            self.send_updates(obj)
        except Exception, e:
            logging.info("unhandle not json format data")