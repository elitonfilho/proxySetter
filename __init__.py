# -*- coding: utf-8 -*-

def classFactory(iface):  # pylint: disable=invalid-name
    from .proxySetter import ProxySetter
    return ProxySetter(iface)
