# -*- coding: utf-8 -*-

import os
import json
import operator
from pathlib import Path
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.gui import *
from qgis.core import *
from PyQt5.QtNetwork import QNetworkProxy, QNetworkProxyFactory, QNetworkAccessManager
from proxySetter import resources
from proxySetter.proxyFactory import ProxyFactory


class ProxySetter:

    def __init__(self, iface):
        self.iface = iface
        self.networkManager = QgsNetworkAccessManager.instance()
        self.s = QSettings()
        jsonPath = Path(__file__).parent.resolve()
        with open(Path(jsonPath, 'config.json'), 'r', encoding='utf-8') as jsonFile:
            self.config = json.load(jsonFile)

    def initGui(self):
        '''Start configurations'''
        self.initActions()

    def initActions(self):
        self.coordinates = []
        # self.toolbar = self.iface.addToolBar(u"Proxy settings")
        self.comboBox = QComboBox()
        self.iface.addToolBarWidget(self.comboBox)
        self.comboBox.addItems([option for option in self.config])

        self.comboBox.activated[str].connect(self.modifyProxy)
        self.comboBox.activated[str].connect(self.updateSettings)

        # iconPath = ':/plugins/proxySetter/proxy.png'
        # self.actionCBox = QAction(QIcon(iconPath), u"Setting proxy", self.iface.mainWindow())

        # self.actionCBox.setStatusTip(None)
        # self.actionCBox.setWhatsThis(None)
        # self.actionCBox.setCheckable(True)

        # self.toolbar.addAction(self.actionCBox)

    def initSignals(self):
        pass

    def getProxy(self, option):
        return QNetworkProxy(QNetworkProxy.HttpProxy,
                             hostName=option['host'],
                             port=option['port'],
                             user=option['user'],
                             password=option['password'])

    def updateSettings(self, text):
        self.s.setValue('proxy/proxyEnabled', 'true')
        self.s.setValue('proxy/proxyHost', self.config[text]['host'])
        self.s.setValue('proxy/proxyPort', self.config[text]['port'])
        self.s.setValue('proxy/proxyUser', self.config[text]['user'])
        self.s.setValue('proxy/proxyPassword', self.config[text]['password'])
        self.s.setValue('proxy/proxyType', self.config[text]['proxyType'])
        # self.s.setValue('proxy/noProxyUrls', )
        self.s.sync()

    def unload(self):
        pass

    def modifyProxy(self, text):
        # After setting the proxy it could be necessary to update active connection. See QGSAuthMethod / QgsAuthManager
        self.proxy = self.getProxy(self.config[text])
        self.proxyFactory = ProxyFactory(self.config[text])
        # for item in self.networkManager.proxyFactories():
        #     self.networkManager.removeProxyFactory(item)
        # self.networkManager.insertProxyFactory(self.proxyFactory)
        # self.networkManager.setProxyFactory(self.proxyFactory)
        QNetworkProxy.setApplicationProxy(self.proxy)
        self.networkManager.setFallbackProxyAndExcludes(self.proxy, [], []) # excludes=self.config[text]['noProxy'], noProxyURLs=self.config[text]['noProxy']
        # self.networkManager.setProxy(self.proxy)
