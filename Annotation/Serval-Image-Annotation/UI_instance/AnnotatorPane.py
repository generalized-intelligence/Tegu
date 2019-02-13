from UI_instance.UI_Model.AnnotatorPane import Ui_AnnotatorPane
from UI_instance.UI_Model.GiiaGraphicsScene import *
from UI_instance.UI_Model.LabelButton import *
from model.AnnotateImageModel import *


class AnnotatorPane(QWidget, Ui_AnnotatorPane):
    """
    Class documentation goes here.
    """
    endAnnotation=pyqtSignal()
    saveToFile=pyqtSignal()
    imageScale=pyqtSignal()
    def __init__(self,Aim:AnnotatedImageModel, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(AnnotatorPane, self).__init__(parent)
        self.imageFilePath = ""
        self.currentImageName = ""
        self.imageFileList = []
        self.imageListModel = QStringListModel()
        self.labelButtons = []
        self.activeLabelId=0
        self.zoomFactor=1
        self.imageLoaded = False
        self.autoFitToView = True
        self.deleting = False
        self.aim = Aim
        self.scene = GiiaGraphicsScene(self)
        self.setupUi(self)
        self.labelButtonListWrapper.setBackgroundRole(QPalette.AlternateBase)
        self.scrollAreaLabelButtons.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.labelButtonLayout.setAlignment(Qt.AlignTop|Qt.AlignHCenter)
        self.graphicsView.setBackgroundRole(QPalette.Dark)
        self.graphicsView.setMouseTracking(True)
        self.graphicsView.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        self.graphicsView.setRenderHint(QPainter.Antialiasing)
        self.graphicsView.setScene(self.scene)
        self.listViewImageNames.setModel(self.imageListModel)
        print("UI_loaded")
        self.aim.annotationChange.connect(self.annotationChangedForImage)
        self.listViewImageNames.doubleClicked.connect(self.loadImageByFileIndex)
        self.listViewImageNames.activated.connect(self.listViewIndexMoved)
        self.scene.mousePositionChange.connect(self.updateMousePosition)
        self.scene.markingBoxStartPoint.connect(self.updateMarkingRegionTopLeft)
        self.scene.markingBoxFinishPoint.connect(self.updateMarkingRegionButtonRight)
        self.scene.markRegionFinish.connect(self.addMarkRegion)
        self.scene.markRegionDeletion.connect(self.updateModel)
        self.scene.deletingModeChanged.connect(self.updateDeleteButtonState)

        self.pushButtonZoomIn.clicked.connect(self.zoomIn)
        self.pushButtonZoomOut.clicked.connect(self.zoomOut)
        self.pushButtonOriginalSize.clicked.connect(self.normalSize)
        self.pushButtonNext.clicked.connect(self.loadNextImage)
        self.pushButtonPrev.clicked.connect(self.loadPrevImage)
        self.pushButtonDel.clicked.connect(self.toggleDeleteMode)
        self.pushButtonSkip.clicked.connect(self.skipCurrentImage)
        self.pushButtonSave.clicked.connect(self.saveButtonPressed)
        self.pushButtonExit.clicked.connect(self.exitButtonPressed)
        self.pushButtonFitInView.clicked.connect(self.fitToView)

        self.pushButtonFitInView.hide()
        self.imageScale.connect(self.imageScaled)

    def loadFile(self,imagePath):
        #此处传入的是完整的文件路径
        reader=QImageReader(imagePath)
        reader.setAutoTransform(True)
        loadImage=reader.read()
        if loadImage is None:
            QMessageBox.information(QGuiApplication.applicationDisplayName(),"无法载入文件:"+imagePath)
            return False
        iw=loadImage.width()
        ih=loadImage.height()
        self.scene.setSceneRect(0,0,iw,ih)
        self.scene.setBackgroundBrush(QBrush(loadImage))
        self.scene.setDeletingMode(False)
        self.fitToView()
        self.graphicsView.centerOn(iw/2,ih/2)
        self.currentImageName=imagePath
        self.showAnnotationsForImage(self.currentImageName)
        self.updateDeleteButtonState()
        self.updateSkipButtonState()
        return True
    def setImageFileList(self,imageList):
        self.imageFileList=imageList
        self.imageListModel.setStringList(self.imageFileList)
        self.updateProgess()
    def setImagePath(self,imagePath):
        pass
    def loadFirstImage(self):
        idx=self.imageListModel.index(0)
        self.listViewImageNames.setCurrentIndex(idx)
        self.updateNavButtonState(0)
        self.loadImageByFileIndex(idx)
    def keyPressEvent(self, event:QKeyEvent):
        if event.key()==Qt.Key_S:
            self.skipCurrentImage()
        elif event.key()==Qt.Key_Right or event.key()==Qt.Key_N:
            self.loadNextImage()
        elif event.key() == Qt.Key_Left or event.key() == Qt.Key_P:
            self.loadPrevImage()
        elif event.key() == Qt.Key_Minus:
            self.zoomOut()
        elif event.key() == Qt.Key_Plus or event.key() == Qt.Key_Equal:
            self.zoomIn()
        elif event.key() == Qt.Key_0:
            self.normalSize()
        elif event.key() == Qt.Key_F7:
            self.showSupportedFormats()
    def updateLabels(self):
        for item in self.labelButtons:
            self.labelButtonList.layout().removeWidget(item)
            item.disconnect()
        self.labelButtons.clear()
        labels=self.aim.getLabels()
        for i in range(len(labels)):
            if i==0:
                continue
            lb=LabelButton(i,labels[i],self)
            lb.setFocusPolicy(Qt.NoFocus)
            lb.setMaximumWidth(75)
            lb.markLabelPressed.connect(self.labelChange)
            self.labelButtonList.layout().addWidget(lb)
            self.labelButtons.append(lb)
    def labelChange(self,labelId:int):
        #print(labelId)
        self.activeLabelId=labelId
        self.scene.setGuideLineColor(ANNOTATION_TAG_COLORS[labelId])
        self.graphicsView.setGuideLineColor(ANNOTATION_TAG_COLORS[labelId])
        self.graphicsView.update()
    def loadNextImage(self):
        idx=self.listViewImageNames.currentIndex()
        #print(idx)
        nextRow=idx.row()+1
        hasNext=self.imageListModel.hasIndex(nextRow,0)
        if hasNext:
            idx=self.imageListModel.index(nextRow)
            self.listViewImageNames.setCurrentIndex(idx)
            self.loadImageByFileIndex(idx)
            self.updateNavButtonState(nextRow)
    def loadPrevImage(self):
        idx = self.listViewImageNames.currentIndex()
        if idx.row()==0:
            return
        prevRow = idx.row() - 1
        hasNext = self.imageListModel.hasIndex(prevRow, 0)
        if hasNext:
            idx = self.imageListModel.index(prevRow)
            self.listViewImageNames.setCurrentIndex(idx)
            self.loadImageByFileIndex(idx)
            self.updateNavButtonState(prevRow)
    def skipCurrentImage(self):
        if self.aim.getAnnotationCountForImage(self.currentImageName)==0:
            return
        self.aim.clearAnnotationForImage(self.currentImageName)
    def listViewIndexMoved(self,index:QModelIndex):
        self.updateNavButtonState(index.row())
    def saveButtonPressed(self):
        self.updateModel()
        self.saveToFile.emit()
    def exitButtonPressed(self):
        self.endAnnotation.emit()
    def annotationChangedForImage(self,imageChanged:str):
        if self.currentImageName==imageChanged:
            self.showAnnotationsForImage(self.currentImageName)
            self.updateDeleteButtonState()
            self.updateSkipButtonState()
        self.updateProgess()
    def loadImageByFileIndex(self,index:QModelIndex):
        self.updateModel()
        row=index.row()
        #print(row)
        #print(self.imageFileList[row])
        self.imageLoaded=self.loadFile(self.imageFileList[row])
        #print(self.imageLoaded)
        if self.imageLoaded:
            self.clearSelectionCoordsDisplay()
    def zoomIn(self):
        self.zoomFactor*=1.25
        if self.zoomFactor>5:
            self.zoomFactor=5
        self.scaleImage()
    def zoomOut(self):
        self.zoomFactor *= 0.8
        if self.zoomFactor <0.1:
            self.zoomFactor = 0.1
        self.scaleImage()
    def normalSize(self):
        self.zoomFactor=1
        self.graphicsView.resetTransform()
        self.imageScale.emit()
    def toggleDeleteMode(self):
        self.scene.setDeletingMode(not self.scene.isDeleting())
        self.scene.update()
    def fitToView(self):
        iw=int(self.scene.width())
        ih=int(self.scene.height())
        self.graphicsView.fitInView(0,0,iw,ih,Qt.KeepAspectRatio)
        vw=self.graphicsView.width()
        vh=self.graphicsView.height()
        hratio=float(vw)/iw
        vratio=float(vh)/ih
        ratio=min([hratio,vratio])
        if ratio>5:
            ratio=5
        if ratio<0.1:
            ratio=0.1
        self.zoomFactor=ratio
        self.imageScale.emit()

    def updateMousePosition(self,pos:QPointF):
        if self.imageLoaded:
            self.lineEditCurPos.setText(" X:"+str(int(pos.x()))+" Y:"+str(int(pos.y())))
    def updateMarkingRegionTopLeft(self,pos:QPointF):
        self.lineEditX1.setText(str(int(pos.x())))
        self.lineEditY1.setText(str(int(pos.y())))
    def updateMarkingRegionButtonRight(self,pos:QPointF):
        self.lineEditX2.setText(str(int(pos.x())))
        self.lineEditY2.setText(str(int(pos.y())))
    def addMarkRegion(self,markRegion:QRectF):
        self.updateModel()
        #print(markRegion)
        if self.activeLabelId==0:
            return
        markRegion=markRegion.normalized()
        if not self.scene.sceneRect().intersects(markRegion):
            return
        x1 = int(max([0,int(markRegion.topLeft().x())]))
        y1 = int(max([0,int(markRegion.topLeft().y())]))
        x2 = int(min([int(self.scene.width()),int(markRegion.bottomRight().x())]))
        y2 = int(min([int(self.scene.height()),int(markRegion.bottomRight().y())]))
        if abs(x2-x1)<MARK_REGION_LOWER_LIMIT or abs(y2-y1)<MARK_REGION_LOWER_LIMIT:
            return
        self.lineEditX1.setText(str(x1))
        self.lineEditY1.setText(str(y1))
        self.lineEditX2.setText(str(x2))
        self.lineEditY2.setText(str(y2))
        self.aim.addAnnotationPara(self.currentImageName,self.activeLabelId,x1,y1,x2,y2)
        #print(self.aim.imgAnnos)
        #print(self.aim.labels)
    def updateModel(self):
        sl=[]
        for item in self.scene.annotationItems():
            sl.append(item.getAnnotationString())
        #print("SL")
        #print(sl)
        if self.aim.getAnnotationCountForImage(self.currentImageName)>-1:
            annotationStringList=[self.currentImageName,",".join(sl)]
            self.aim.updateAnnotationByString(annotationStringList)
    def showSupportedFormats(self):
        fmts=", ".join(SUPPORTED_FILE_FORMATS_LIST)
        QMessageBox.information(self,"支持的文件格式",fmts,QMessageBox.Ok)
    def imageScaled(self):
        self.scene.resetCursorPos()
        self.graphicsView.update()
        self.updateZoomButtonStates()
    def updateDeleteButtonState(self):
        self.pushButtonDel.setEnabled(self.aim.getAnnotationCountForImage(self.currentImageName)>0)
        if self.scene.isDeleting():
            str_text="Done"
        else:
            str_text="Delete"
        self.pushButtonDel.setText(str_text)
    def scaleImage(self):
        trans=QTransform()
        trans.scale(self.zoomFactor,self.zoomFactor)
        self.graphicsView.setTransform(trans)
        self.imageScale.emit()
    def updateZoomButtonStates(self):
        self.pushButtonZoomIn.setEnabled(self.zoomFactor < 5)
        self.pushButtonZoomOut.setEnabled(self.zoomFactor > 0.1)
        self.pushButtonOriginalSize.setEnabled(self.zoomFactor != 1)
    def showAnnotationsForImage(self,fileName:str):
        self.scene.clearAnnotationItems()
        if self.aim.getAnnotationCountForImage(self.currentImageName)<0:
            self.graphicsView.setSkipMode(False)
            return
        annos=self.aim.getAnnotationsForImage(fileName)
        if len(annos)==0:
            self.graphicsView.setSkipMode(True)
            self.scene.setDeletingMode(False)
        else:
            self.graphicsView.setSkipMode(False)
            for anno in annos:
                rect=QRectF(0,0,abs(anno.x2-anno.x1),abs(anno.y2-anno.y1))
                rectItem=AnnotationGraphicsItem(rect,anno.labelId)
                self.scene.addAnnotationItem(rectItem)
                rectItem.setPos(anno.x1,anno.y1)
    def updateNavButtonState(self,currentImageIndex:int):
        self.pushButtonPrev.setEnabled(currentImageIndex>0)
        self.pushButtonNext.setEnabled(currentImageIndex<self.imageListModel.rowCount()-1)
    def updateSkipButtonState(self):
        self.pushButtonSkip.setDisabled(self.aim.getAnnotationCountForImage(self.currentImageName)==0)
    def updateProgess(self):
        self.lineEditProgress.setText(str(self.aim.getAnnotatedImageCount())+" / "+str(len(self.imageFileList)))
    def clearSelectionCoordsDisplay(self):
        self.lineEditX1.clear()
        self.lineEditX2.clear()
        self.lineEditY1.clear()
        self.lineEditY2.clear()

