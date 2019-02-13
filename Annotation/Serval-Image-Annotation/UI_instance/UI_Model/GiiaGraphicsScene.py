from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from enum import Enum
from config.defaults import *
from model.ImageAnnotation import Annotation
from model.AnnotationGraphicsItem import *
class GiiaGraphicsScene(QGraphicsScene):
    mousePositionChange=pyqtSignal(QPointF)
    markingBoxStartPoint=pyqtSignal(QPointF)
    markingBoxFinishPoint=pyqtSignal(QPointF)
    markRegionFinish=pyqtSignal(QRectF)
    markRegionDeletion=pyqtSignal()
    deletingModeChanged=pyqtSignal(bool)
    def __init__(self,parent):
        super(GiiaGraphicsScene, self).__init__(parent=parent)
        self.lastPoint=QPointF()
        self.cursorPos=QPointF()
        self.guideColor=QColor()
        self.curX=-1
        self.curY=-1
        self.marking=False
        self.movingItem=False
        self.resizing=False
        self.deleting=False
        self.annoItems=[]
    def isMarking(self):
        return self.marking
    def isMoving(self):
        return self.movingItem
    def isDeleting(self):
        return self.deleting
    def annotationItemMoved(self,annotation:Annotation,newPosition:QPointF):
        pass
    def annotationItems(self):
        return self.annoItems
    def addAnnotationItem(self,item:AnnotationGraphicsItem):
        item.setDeleting(self.deleting)
        self.annoItems.append(item)
        self.addItem(item)
    def removeAnnotationItem(self,item:AnnotationGraphicsItem):
        temp_anno=[anno for anno in self.annoItems if anno != item]
        #print(temp_anno)
        self.annoItems.clear()
        self.annoItems.extend(temp_anno)
        #print(self.annoItems)
        self.removeItem(item)

    def clearAnnotationItems(self):
        for item in self.annoItems:
            self.removeItem(item)
        self.annoItems.clear()
    def cursorPosition(self):
        return self.cursorPos
    def lastCursorPosition(self):
        return self.lastPoint
    def drawBackground(self, painter: QPainter, rect: QRectF):
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        painter.drawImage(0,0,self.backgroundBrush().textureImage())
    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if event.button()!=Qt.LeftButton:
            event.accept()
            return
        super(GiiaGraphicsScene, self).mousePressEvent(event)
        if event.isAccepted() and len(self.selectedItems())>0:
            self.movingItem=True
            self.mouseMoveEvent(event)
            return
        self.movingItem=False
        self.marking=False
        item=self.itemAt(event.scenePos(),QTransform())
        if item is not None:
            return
        self.lastPoint=event.scenePos()
        self.marking=True
        self.update()
        self.markingBoxStartPoint.emit(self.lastPoint)
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        super(GiiaGraphicsScene, self).mouseMoveEvent(event)
        self.cursorPos=event.scenePos()
        if self.movingItem:
            if len(self.selectedItems()) >0:
                item=self.selectedItems()[0]
                self.markingBoxStartPoint.emit(item.scenePos())
                self.markingBoxFinishPoint.emit(item.mapToScene(item.boundingRect().bottomRight()))
        else:
            self.mousePositionChange.emit(self.cursorPos)
        if self.marking:
            self.markingBoxFinishPoint.emit(self.cursorPos)
        self.update()


    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        if event.button()!=Qt.LeftButton:
            event.accept()
            return
        if self.deleting and len(self.selectedItems()) >0:
            item=self.selectedItems()[0]
            if item and item.hasDeleteButtonUnderCursor():
                print("deleting")
                print(item)
                self.removeAnnotationItem(item)
                self.markRegionDeletion.emit()
                self.update()
                event.accept()
        super(GiiaGraphicsScene, self).mouseReleaseEvent(event)
        if event.isAccepted():
            return
        if self.movingItem:
            self.movingItem=False
            self.mouseMoveEvent(event)
            return
        if self.marking:
            finPoint=event.scenePos()
            markRegion=QRectF(self.lastPoint,finPoint)
            self.marking=False
            self.mouseMoveEvent(event)
            self.markRegionFinish.emit(markRegion.normalized())
            return
    def setGuideLineColor(self,color:QColor):
        self.guideColor=color
        self.update()
    def resetCursorPos(self):
        self.cursorPos.setX(-32767)
        self.cursorPos.setY(-32767)
    def setDeletingMode(self,mode:bool):
        self.deleting=mode
        for item in self.annoItems:
            item.setDeleting(self.deleting)
        self.deletingModeChanged.emit(self.deleting)
