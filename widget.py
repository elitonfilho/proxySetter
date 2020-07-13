from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QFormLayout, QPushButton
from PyQt5.QtCore import pyqtSignal


class Widget(QWidget):

    triggerUpdate = pyqtSignal(str)

    def __init__(self, text):
        super().__init__()
        self.txt = text
        layout = QFormLayout()
        btn = QPushButton("Enviar dados")
        btn.clicked.connect(self.getItem)
        label_username = QLabel('Insira o usuário do Proxy do CTA:')
        self.username = QLineEdit()
        label_password = QLabel('Insira a senha do Proxy do CTA:')
        self.password = QLineEdit()
        self.password.setEchoMode(2)

        layout.addRow(label_username)
        layout.addRow(self.username)
        layout.addRow(label_password)
        layout.addRow(self.password)
        layout.addRow(btn)

        self.setLayout(layout)

        self.setWindowTitle('Inserir dados do Proxy CTA')

        self.show()

    def getItem(self):
        self.triggerUpdate.emit(self.txt)
        self.close()
