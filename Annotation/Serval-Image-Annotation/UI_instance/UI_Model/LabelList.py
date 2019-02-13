from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
class LabelList(QWidget):
    def __init__(self,parent=None):
        super(LabelList, self).__init__(parent)
        self.layout=QGridLayout()

        self.labelWidgets=[]
        self.setupUi(self)
    def setupUi(self):
        self.layout.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        items_wrapper=QWidget(self)
        items_wrapper.setLayout(self.layout)
        scrollArea = QScrollArea(self)
        scrollArea.setMinimumHeight(400)
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(items_wrapper)
        outer_layout = QVBoxLayout(self)
        outer_layout.addWidget(scrollArea)
        self.setLayout(outer_layout)
        self.setBackgroundRole(QPalette.AlternateBase)