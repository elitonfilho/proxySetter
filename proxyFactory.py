from PyQt5.QtNetwork import QNetworkProxyFactory, QNetworkProxy

class ProxyFactory(QNetworkProxyFactory):

    def __init__(self, config):
        super().__init__()
        self.config = config
        
    def queryProxy(self, query):
        return [QNetworkProxy(QNetworkProxy.HttpProxy,
                             hostName=self.config['host'],
                             port=self.config['port'],
                             user=self.config['user'],
                             password=self.config['password'])]

