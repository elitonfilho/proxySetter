# -*- coding: utf-8 -*-

import os, json
from pathlib import Path
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.gui import *
from qgis.core import *
from proxySetter import resources


class ProxySetter:

    def __init__(self, iface):
        self.iface = iface
        jsonPath = Path(__file__).parent.resolve()
        with open(Path(jsonPath, 'config.json'), 'r', encoding='utf-8') as jsonFile:
            self.config = json.load(jsonFile)

    def initGui(self):
        '''Start configurations'''
        self.initActions()
        self.initSignals()

    def initActions(self):
        self.coordinates = []
        self.toolbar = self.iface.addToolBar(u"Proxy settings")
        self.comboBox = QComboBox(self.toolbar)
        (print(data) for data in self.config)

        # iconPath = ':/plugins/proxySetter/proxy.png'
        # self.actionCBox = QAction(QIcon(iconPath), u"Setting proxy", self.iface.mainWindow())

        # self.actionCBox.setStatusTip(None)
        # self.actionCBox.setWhatsThis(None)
        # self.actionCBox.setCheckable(True)

        # self.toolbar.addAction(self.actionCBox)

    def initSignals(self):
        pass

    def unload(self):
        pass

