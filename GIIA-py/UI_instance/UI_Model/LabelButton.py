from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from config.defaults import *
class LabelButton(QPushButton):
    def __init__(self,labelId:int,text:str,parent):
        super(LabelButton, self).__init__(parent)
        self.setStyleSheet("text-align: left; min-width:80;")
        self.id=labelId
        self.color=ANNOTATION_TAG_COLORS[self.id%9]
        pix=QPixmap(8,16)
        ptr=QPainter(pix)
        ptr.setBrush(self.color)
        ptr.drawRect(0,0,pix.width(),pix.height())
        icon=QIcon(pix)
        self.setIcon(icon)
        self.setText(text)
        self.clicked.connect(self.buttonPressed)
        ptr.end()
    def buttonPressed(self):
        print("my id is"+str(self.id))
        self.markLabelPressed.emit(self.id)
    markLabelPressed=pyqtSignal(int)