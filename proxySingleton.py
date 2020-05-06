# -*- coding: utf-8 -*-

from PyQt5.QtNetwork import QNetworkProxy

class ProxySingleton:

    proxy = None

    @staticmethod
    def getInstance():
        if not ProxySingleton.proxy:
            ProxySingleton.proxy = QNetworkProxy()
        return ProxySingleton.proxy