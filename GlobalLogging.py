import logging
from PyQt5 import QtCore

from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import *


class QTextBrowserHanlder(logging.Handler):
    def __init__(self, main_window):
        super().__init__()
        self.console_win = main_window.console_win
        self.main_window=main_window
        #self.cursor = self.console_win.textCursor()


    def emit(self, record):
        msg = self.format(record)
        self.console_win.append(msg)
        #self.cursor.movePosition(QTextCursor.End)
        #self.console_win.setTextCursor(self.cursor)
        self.main_window._signal.emit()

class NullHandler(logging.Handler):
    def emit(self, record): pass


class GlobalLogging:
    log = None

    @staticmethod
    def getInstance():
        if GlobalLogging.log == None:
            GlobalLogging.log = GlobalLogging()
        return GlobalLogging.log

    def __init__(self):
        self.logger = None
        self.handler = None
        self.level = logging.INFO
        self.logger = logging.getLogger("GlobalLogging")
        self.formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
        h = NullHandler()
        self.logger.addHandler(h)

    def setLoggingToFile(self, file):
        fh = logging.FileHandler(file)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

    def setLoggingToConsole(self):
        ch = logging.StreamHandler()
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

    def setLoggingToQTextBrowserHanlder(self, main_window):
        qt_hanlder = QTextBrowserHanlder(main_window)
        qt_hanlder.setFormatter(self.formatter)
        self.logger.addHandler(qt_hanlder)

    def setLoggingLevel(self, level):
        self.level = level
        self.logger.setLevel(level)

    def debug(self, s):
        self.logger.debug(s)
        if not self.handler == None and self.level <= logging.DEBUG:
            print(logging.DEBUG)
            print(self.level)
            self.handler('debug:' + s)

    def info(self, s):
        self.logger.info(s)
        if not self.handler == None and self.level <= logging.INFO:
            self.handler('info:' + s)

    def warn(self, s):
        self.logger.warn(s)
        if not self.handler == None and self.level <= logging.WARNING:
            self.handler('warn:' + s)

    def error(self, s):
        self.logger.error(s)
        if not self.handler == None and self.level <= logging.ERROR:
            self.handler('error:' + s)

    def critical(self, s):
        self.logger.critical(s)
        if not self.handler == None and self.level <= logging.CRITICAL:
            self.handler('critical:' + s)
