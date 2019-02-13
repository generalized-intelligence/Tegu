from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from enum import Enum
from config.defaults import *
Offset=3
Delbtnoffset=8
class enum(Enum):
    Top = 0x1,
    Bottom = 0x2,
    Left = 0x4,
    TopLeft = 0x1 | 0x4,
    BottomLeft = 0x2 | 0x4,
    Right = 0x8,
    TopRight = 0x1 | 0x8,
    BottomRight = 0x2 | 0x8

class HandleItem(QGraphicsRectItem):
    handleItemBrush = QBrush(Qt.black)
    handleItemPen = QPen(Qt.NoPen)
    def __init__(self,positionFlag,parent):
        self.posFlag=positionFlag
        self.parentAnnoItem=parent
        super(HandleItem,self).__init__(-4,-4,8,8,parent=parent)
        self.setZValue(0)
        self.setOpacity(0.85)
        self.setBrush(self.handleItemBrush)
        self.setPen(self.handleItemPen)
        self.setFlag(self.ItemIgnoresTransformations)

    def getPositionFlag(self):
        return self.posFlag
    def restrictPosition(self,newPos):
        pass
class DeleteButton(QGraphicsRectItem):
    deleteButtonPen=QPen(Qt.NoPen)
    deleteButtonStrokePen=QPen(Qt.white,2,Qt.SolidLine,Qt.RoundCap)
    deleteButtonStrokePenHover=QPen(Qt.red,2,Qt.SolidLine,Qt.RoundCap)
    deleteButtonBrush=QBrush(Qt.black)
    def __init__(self,parent):
        self.parentAnnoItem=parent
        self.active=False
        super(DeleteButton, self).__init__(-15, -0, 15, 15, parent=parent)
        self.setZValue(0)
        self.setBrush(self.deleteButtonBrush)
        self.setPen(self.deleteButtonPen)
        self.setFlag(self.ItemIgnoresTransformations)

    def setActive(self, value: bool):
        self.active=value
    def paint(self,painter:QPainter,option:QStyleOptionGraphicsItem,widget:QWidget):
        if not self.parentAnnoItem.isDeleting():
            return
        super(DeleteButton, self).paint(painter,option,widget)
        if self.active:
            painter.setPen(self.deleteButtonStrokePenHover)
        else:
            painter.setPen(self.deleteButtonStrokePen)
        painter.drawLine(-11, 4, -4, 11)
        painter.drawLine(-4, 4, -11, 11)



class AnnotationGraphicsItem(QGraphicsRectItem):
    def __init__(self,rectF:QRectF,labelId:int,parent=None):
        self.annotationLabelId=labelId
        self.resizePosFlag=0
        self.resizing=False;
        self.deleting=False;
        self.deleteButtonUnderCursor=False;
        self.resizeRefPoint=QPointF()
        self.fillColor=ANNOTATION_TAG_COLORS[labelId%9]
        self.fillColor.setAlpha(128)
        self.handles=[]
        self.DeleteButton=None
        super(AnnotationGraphicsItem,self).__init__(rectF,parent)
        self.setFlags(QGraphicsItem.ItemIsMovable|QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)
        self.setAcceptHoverEvents(True)
        self.setPen(QPen(Qt.NoPen))
        self.setBrush(QBrush(self.fillColor))
        self.setZValue(1)
        self.handles.append(HandleItem(enum.TopLeft,self))
        self.handles.append(HandleItem(enum.Top, self))
        self.handles.append(HandleItem(enum.TopRight, self))
        self.handles.append(HandleItem(enum.Right, self))
        self.handles.append(HandleItem(enum.BottomRight, self))
        self.handles.append(HandleItem(enum.Bottom, self))
        self.handles.append(HandleItem(enum.BottomLeft, self))
        self.handles.append(HandleItem(enum.Left, self))
        self.deleteButton=DeleteButton(self)
        self.updateHandleItemPositions()
        self.hideHandles()
    def updateHandleItemPositions(self):
        for h in self.handles:
            if h.getPositionFlag()==enum.TopLeft:
                h.setPos(self.rect().left()+Offset,self.rect().top()+Offset)
            elif h.getPositionFlag() == enum.Top:
                h.setPos(self.rect().left() + self.rect().width() / 2 - 1, self.rect().top() + Offset);
            elif h.getPositionFlag() == enum.TopRight:
                h.setPos(self.rect().right() - Offset, self.rect().top() + Offset);
            elif h.getPositionFlag() == enum.Right:
                h.setPos(self.rect().right() - Offset, self.rect().top() + self.rect().height() / 2 - 1);
            elif h.getPositionFlag() == enum.BottomRight:
                h.setPos(self.rect().right() - Offset, self.rect().bottom() - Offset);
            elif h.getPositionFlag() == enum.Bottom:
                h.setPos(self.rect().left() + self.rect().width() / 2 - 1, self.rect().bottom() - Offset);
            elif h.getPositionFlag() == enum.BottomLeft:
                h.setPos(self.rect().left() + Offset, self.rect().bottom() - Offset);
            elif h.getPositionFlag() == enum.Left:
                h.setPos(self.rect().left() + Offset, self.rect().top() + self.rect().height() / 2 - 1);
        self.deleteButton.setPos(self.rect().right() - Delbtnoffset, self.rect().top() + Delbtnoffset)
    def itemChange(self, change, value):
        if not self.scene():
            return super(AnnotationGraphicsItem, self).itemChange(change,value)
        if change == QGraphicsItem.ItemPositionChange:
            newPos=QPointF(value)
            srect=self.scene().sceneRect()
            #print(srect)
            if not srect.contains(QRectF(newPos,self.rect().size())):
                # Keep the item inside the scene rect.
                newPos.setX(min([srect.right() - self.rect().width(), max([newPos.x(), srect.left()])]))
                newPos.setY(min([srect.bottom() - self.rect().height(), max([newPos.y(), srect.top()])]))
                return newPos
        elif change==QGraphicsItem.ItemSelectedChange:
            if bool(value):
                # selected
                self.setBrush(QBrush(self.fillColor.lighter()))
                self.showHandles()
                self.setZValue(2)
            else:
                # not selected
                self.setBrush(QBrush(self.fillColor))
                self.hideHandles()
                self.setZValue(1)
        return super(AnnotationGraphicsItem, self).itemChange(change,value)
    def mousePressEvent(self, mouseEvent: QGraphicsSceneMouseEvent):
        if mouseEvent.modifiers() and Qt.ControlModifier:
            mouseEvent.accept()
            return
        if self.rect().contains(mouseEvent.pos()) and len(self.scene().views())>0:
            trans=self.scene().views()[0].transform()
            curPos=self.deviceTransform(trans).map(mouseEvent.pos())
            for h in self.handles:
                if h.deviceTransform(trans).map(QPolygonF(h.rect())).containsPoint(curPos,Qt.OddEvenFill):
                    self.resizing=True
                    self.resizePosFlag=h.getPositionFlag()
                    break
                self.resizing=False
            if self.resizing:
                if self.resizePosFlag==enum.TopLeft or self.resizePosFlag==enum.Top:
                    self.resizeRefPoint=self.rect().bottomRight()
                elif self.resizePosFlag==enum.TopRight or self.resizePosFlag==enum.Right:
                    self.resizeRefPoint=self.rect().bottomLeft()
                elif self.resizePosFlag==enum.BottomRight or self.resizePosFlag==enum.Bottom:
                    self.resizeRefPoint=self.rect().topLeft()
                elif self.resizePosFlag==enum.BottomLeft or self.resizePosFlag==enum.Left:
                    self.resizeRefPoint=self.rect().topRight()
                self.resizeRefPoint=self.mapToScene(self.resizeRefPoint)
                mouseEvent.accept()
                return
        super(AnnotationGraphicsItem, self).mousePressEvent(mouseEvent)

    def mouseReleaseEvent(self, mouseEvent: QGraphicsSceneMouseEvent):
        super(AnnotationGraphicsItem, self).mouseReleaseEvent(mouseEvent)
        self.resizing=False
        self.resizePosFlag=0
    def mouseMoveEvent(self, mouseEvent: 'QGraphicsSceneMouseEvent'):
        if not self.scene().sceneRect().contains(mouseEvent.scenePos()):
            mouseEvent.accept()
            return
        curPos=mouseEvent.scenePos()
        x=self.scenePos().x()
        y = self.scenePos().y()
        w=self.rect().width()
        h = self.rect().height()
        if self.resizing:
            minimun=MARK_REGION_LOWER_LIMIT*2
            xUnderflow=False
            yUnderflow=False
            if self.resizePosFlag==enum.TopLeft:
                xUnderflow = curPos.x() > (self.resizeRefPoint.x() - minimun);
                yUnderflow = curPos.y() > (self.resizeRefPoint.y() - minimun);
                w = minimun if xUnderflow else self.resizeRefPoint.x() - curPos.x();
                h = minimun if yUnderflow else self.resizeRefPoint.y() - curPos.y();
                x = self.resizeRefPoint.x() - minimun if xUnderflow else curPos.x();
                y = self.resizeRefPoint.y() - minimun if yUnderflow else curPos.y();
                self.setCursor(Qt.SizeFDiagCursor)
            elif self.resizePosFlag==enum.Top:
                yUnderflow = curPos.y() > (self.resizeRefPoint.y() - minimun);
                y = self.resizeRefPoint.y() - minimun if yUnderflow else curPos.y();
                h = minimun if yUnderflow else self.resizeRefPoint.y() - curPos.y();
                self.setCursor(Qt.SizeVerCursor);
            elif self.resizePosFlag==enum.TopRight:
                xUnderflow = curPos.x() < (self.resizeRefPoint.x() + minimun);
                yUnderflow = curPos.y() > (self.resizeRefPoint.y() - minimun);
                w = minimun if xUnderflow else curPos.x() - self.resizeRefPoint.x();
                h = minimun if yUnderflow else self.resizeRefPoint.y() - curPos.y();
                x = self.resizeRefPoint.x() if xUnderflow else curPos.x() - w;
                y = self.resizeRefPoint.y() -  minimun if yUnderflow else curPos.y();
                self.setCursor(Qt.SizeBDiagCursor);
            elif self.resizePosFlag == enum.Right:
                xUnderflow = curPos.x() < (self.resizeRefPoint.x() + minimun);
                w = minimun if xUnderflow  else  curPos.x() - self.resizeRefPoint.x()
                x = self.resizeRefPoint.x() if xUnderflow  else  curPos.x() - w
                self.setCursor(Qt.SizeHorCursor);
            elif self.resizePosFlag == enum.BottomRight:
                xUnderflow = curPos.x() < (self.resizeRefPoint.x() + minimun);
                yUnderflow = curPos.y() < (self.resizeRefPoint.y() + minimun);
                w = minimun if xUnderflow  else  (curPos.x() - self.resizeRefPoint.x())
                h = minimun if yUnderflow  else  (curPos.y() - self.resizeRefPoint.y())
                x = self.resizeRefPoint.x();
                y = self.resizeRefPoint.y();
                self.setCursor(Qt.SizeFDiagCursor);
            elif self.resizePosFlag == enum.Bottom:
                yUnderflow = curPos.y() < (self.resizeRefPoint.y() + minimun);
                h = minimun if yUnderflow  else  (curPos.y() - self.resizeRefPoint.y())
                y = self.resizeRefPoint.y();
                self.setCursor(Qt.SizeVerCursor);
            elif self.resizePosFlag == enum.BottomLeft:
                xUnderflow = curPos.x() > (self.resizeRefPoint.x() - minimun);
                yUnderflow = curPos.y() < (self.resizeRefPoint.y() + minimun);
                w = minimun if xUnderflow  else  (self.resizeRefPoint.x() - curPos.x())
                h = minimun if yUnderflow  else  (curPos.y() - self.resizeRefPoint.y())
                x = self.resizeRefPoint.x() - w;
                y = self.resizeRefPoint.y();
                self.setCursor(Qt.SizeBDiagCursor);
            elif self.resizePosFlag == enum.Left:
                xUnderflow = curPos.x() > (self.resizeRefPoint.x() - minimun);
                w = minimun if xUnderflow  else  (self.resizeRefPoint.x() - curPos.x())
                x = self.resizeRefPoint.x() - w;
                self.setCursor(Qt.SizeHorCursor);
            self.setRect(0,0,w,h)
            self.setPos(x,y)
            self.updateHandleItemPositions()
        else:
            super(AnnotationGraphicsItem, self).mouseMoveEvent(mouseEvent)
            self.setCursor(Qt.ClosedHandCursor)
    def hoverMoveEvent(self, hoverEvent:QGraphicsSceneHoverEvent):
        if not self.isSelected():
            return
        trans = self.scene().views()[0].transform()
        curPos = self.deviceTransform(trans).map(hoverEvent.pos())
        for h in self.handles:
            if h.deviceTransform(trans).map(QPolygonF(h.rect())).containsPoint(curPos,Qt.OddEvenFill):
                self.resizePosFlag=h.getPositionFlag()
                break
            self.resizePosFlag=0
        if self.resizePosFlag==enum.Top:
            pass
        elif self.resizePosFlag==enum.Bottom:
            self.setCursor(Qt.SizeVerCursor)
        elif self.resizePosFlag==enum.Left:
            pass
        elif self.resizePosFlag==enum.Right:
            self.setCursor(Qt.SizeHorCursor)
        elif self.resizePosFlag==enum.TopLeft:
            pass
        elif self.resizePosFlag==enum.BottomRight:
            self.setCursor(Qt.SizeFDiagCursor)
        elif self.resizePosFlag==enum.TopRight:
            pass
        elif self.resizePosFlag==enum.BottomLeft:
            self.setCursor(Qt.SizeBDiagCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
        onDelBtn=self.deleteButton.deviceTransform(trans).map(QPolygonF(self.deleteButton.rect())).containsPoint(curPos,Qt.OddEvenFill)
        if onDelBtn!=self.deleteButtonUnderCursor:
            self.deleteButtonUnderCursor=onDelBtn
            self.deleteButton.setActive(self.deleteButtonUnderCursor)
            self.update(self.rect().right()-15-Delbtnoffset,0,15+Delbtnoffset,15+Delbtnoffset)
    def updateHandleItemPositions(self):
        for h in self.handles:
            if h.getPositionFlag()==enum.TopLeft:
                h.setPos(self.rect().left() + Offset, self.rect().top() + Offset);
            elif h.getPositionFlag() == enum.Top:
                h.setPos(self.rect().left() + self.rect().width() / 2 - 1, self.rect().top() + Offset);
            elif h.getPositionFlag() == enum.TopRight:
                h.setPos(self.rect().right() - Offset, self.rect().top() + Offset);
            elif h.getPositionFlag() == enum.Right:
                h.setPos(self.rect().right() - Offset, self.rect().top() + self.rect().height() / 2 - 1);
            elif h.getPositionFlag() == enum.BottomRight:
                h.setPos(self.rect().right() - Offset, self.rect().bottom() - Offset);
            elif h.getPositionFlag()==enum.Bottom:
                h.setPos(self.rect().left() + self.rect().width() / 2 - 1, self.rect().bottom() - Offset);
            elif h.getPositionFlag()==enum.BottomLeft:
                h.setPos(self.rect().left() + Offset, self.rect().bottom() - Offset);
            elif h.getPositionFlag()==enum.Left:
                h.setPos(self.rect().left() + Offset, self.rect().top() + self.rect().height() / 2 - 1);
        self.deleteButton.setPos(self.rect().right()-Delbtnoffset,self.rect().top()+Delbtnoffset)
    def isDeleting(self):
        return self.deleting
    def setDeleting(self,value:bool):
        self.deleting=value
    def getAnnotationString(self):
        x1=int(self.scenePos().x())
        y1=int(self.scenePos().y())
        x2=x1+self.rect().width()
        y2=y1+self.rect().height()
        str_result="{},{},{},{},{}".format(self.annotationLabelId,x1,y1,x2,y2)
        return str_result
    def showHandles(self):
        for h in self.handles:
            h.setVisible(True)
    def hideHandles(self):
        for h in self.handles:
            h.setVisible(False)
    def hasDeleteButtonUnderCursor(self):
        return self.deleteButtonUnderCursor
