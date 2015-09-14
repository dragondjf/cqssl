#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import *

class SignalManager(QObject):

    statusTextChanged = pyqtSignal("QString")

    def __init__(self, parent=None):
        super(SignalManager, self).__init__()

signalManager = SignalManager()