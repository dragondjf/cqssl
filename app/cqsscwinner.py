#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from cqsscworker import CqsscWorker
from signalmanager import signalManager
    

class CqsscWinner(QMainWindow):

    def __init__(self, parent=None):
        super(CqsscWinner, self).__init__(parent)
        self.resize(800, 600)
        self.initWorker()
        self.initConnect()

    def initWorker(self):
        self.worker = CqsscWorker()
        self.workerThread = QThread()
        self.worker.moveToThread(self.workerThread)
        self.workerThread.start()
        self.workerThread.started.connect(self.worker.analyzeData)
        # self.workerThread.started.connect(self.worker)

    def initConnect(self):
        signalManager.statusTextChanged.connect(self.statusBar().showMessage)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    cq = CqsscWinner()
    cq.show()
    app.exec_()