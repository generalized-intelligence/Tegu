from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from UI_instance.UI_Model.GiiaGraphicsScene import GiiaGraphicsScene
from config.defaults import *


class GraphicsView(QGraphicsView):
    def __init__(self,parent=None):
        super(GraphicsView, self).__init__(parent=parent)
        self.scene=None
        self.guideLinePen=QPen()
        self.cursorPos=QPointF()
        self.skipMode=False
    def setScene(self, scene: GiiaGraphicsScene):
        self.scene=scene
        super(GraphicsView, self).setScene(scene)
        self.guideLinePen.setWidth(0)
        self.guideLinePen.setBrush(Qt.black)
    def setSkipMode(self,value:bool):
        self.skipMode=value
        self.scene.update()
    def setGuideLineColor(self,color:QColor):
        self.guideLinePen.setColor(color)
    def paintEvent(self, event: QPaintEvent):
        super(GraphicsView, self).paintEvent(event)
        ptr=QPainter(self.viewport())
        ptr.setPen(self.guideLinePen)
        cursorPos=self.scene.cursorPosition()
        #print(cursorPos)
        cursorPos=self.mapFromScene(cursorPos)
        if self.scene.isMarking():
            #print("marking")
            lastCursorPos=self.scene.lastCursorPosition()
            lastCursorPos=self.mapFromScene(lastCursorPos)
            #print(lastCursorPos)
            #print(cursorPos)
            ptr.drawRect(QRectF(lastCursorPos,cursorPos).normalized())
        elif self.scene.isMoving():
            pass
            #print("moving")
        else:
            ptr.drawLine(0, cursorPos.y(), self.width(), cursorPos.y());
            ptr.drawLine(cursorPos.x(), 0, cursorPos.x(), self.height());
        if self.skipMode:
            ptr.setRenderHints(self.renderHints())
            brush=QBrush(Qt.yellow)
            brush.setStyle(Qt.BDiagPattern)
            ptr.setBrush(brush)
            ptr.drawRect(0,0,self.width(),self.height())