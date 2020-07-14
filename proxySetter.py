# -*- coding: utf-8 -*-

import os
import json
import base64
from pathlib import Path
from qgis.PyQt.QtWidgets import QComboBox
from qgis.PyQt.QtNetwork import QNetworkProxy, QNetworkProxyFactory
from qgis.core import QgsSettings, QgsNetworkAccessManager
from proxySetter import resources
from proxySetter.proxyFactory import ProxyFactory
from proxySetter.widget import Widget


class ProxySetter:

    def __init__(self, iface):
        self.iface = iface
        self.networkManager = QgsNetworkAccessManager.instance()
        self.s = QgsSettings()
        self.jsonPath = Path(__file__).parent.resolve() / 'config.json'
        with open(self.jsonPath, 'r', encoding='utf-8') as jsonFile:
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

        self.comboBox.activated[str].connect(self.handler)
        # self.comboBox.activated[str].connect(self.modifyProxy)

        # iconPath = ':/plugins/proxySetter/proxy.png'
        # self.actionCBox = QAction(QIcon(iconPath), u"Setting proxy", self.iface.mainWindow())

        # self.actionCBox.setStatusTip(None)
        # self.actionCBox.setWhatsThis(None)
        # self.actionCBox.setCheckable(True)

        # self.toolbar.addAction(self.actionCBox)

    def initSignals(self):
        pass

    def getPasswordB64(self, text):
        temp = base64.b64decode(bytes(text['password'], 'utf-8'))
        return temp.decode('utf-8')

    def getProxy(self, option):
        return QNetworkProxy(QNetworkProxy.HttpProxy,
                             hostName=option['host'],
                             port=option['port'],
                             user=option['user'],
                             password=self.getPasswordB64(option))

    def handler(self, text):
        print(self.config[text])
        if not (self.config[text]['user'] or self.config[text]['password']):
            self.widget = Widget(text)
            self.widget.triggerUpdate[str].connect(self.updateUnknown)
        else:
            self.updateSettings(text)
            self.modifyProxy(text)

    def updateSettings(self, text):
        self.s.setValue('proxy/proxyEnabled', 'true')
        self.s.setValue('proxy/proxyHost', self.config[text]['host'])
        self.s.setValue('proxy/proxyPort', self.config[text]['port'])
        self.s.setValue('proxy/proxyUser', self.config[text]['user'])
        self.s.setValue('proxy/proxyPassword',
                        self.getPasswordB64(self.config[text]))
        self.s.setValue('proxy/proxyType', self.config[text]['proxyType'])
        self.s.setValue('proxy/noProxyUrls', self.config[text]['noProxy'])
        self.s.sync()

    def updateUnknown(self, text):
        print('oui!!!')
        self.config[text]['user'] = self.widget.password.text()
        self.config[text]['password'] = base64.b64encode(
            bytes(self.widget.password.text(), 'utf-8')).decode('utf-8')
        self.handler(text)
        with open(self.jsonPath, 'w') as f:
            json.dump(self.config, f)

    def unload(self):
        pass

    def modifyProxy(self, text):
        # After setting the proxy it could be necessary to update active connection. See QGSAuthMethod / QgsAuthManager
        self.proxy = self.getProxy(self.config[text])
        QNetworkProxy.setApplicationProxy(self.proxy)
        # excludes=self.config[text]['noProxy'], noProxyURLs=self.config[text]['noProxy']
        self.networkManager.setFallbackProxyAndExcludes(
            self.proxy, [], self.config[text]['noProxy'])
        # self.networkManager.setProxy(self.proxy)
        '''
        Option for proxyFactory:
        self.proxyFactory = ProxyFactory(self.config[text])
        for item in self.networkManager.proxyFactories():
            self.networkManager.removeProxyFactory(item)
        self.networkManager.insertProxyFactory(self.proxyFactory)
        self.networkManager.setProxyFactory(self.proxyFactory)
        '''
