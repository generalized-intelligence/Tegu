from model.ImageAnnotation import Annotation

from PyQt5.QtCore import QObject , pyqtSignal
Check_header="aimg"
Label_line_header="0:__background__"
Label_line_header_len=len(Label_line_header)
class AnnotatedImageModel(QObject):
    labelChange=pyqtSignal()
    annotationChange=pyqtSignal(str)
    def __init__(self,parent=None):
        super().__init__(parent)
        self.imgAnnos=dict()#QMap<QString, QMap<QString, Annotation>> imgAnnos;
        self.labels=[]#QVector<QString> labels;
    def getImageFiles(self):
        return list(self.imgAnnos.keys())
    def initWithSerializeString(self,serializeString):
        if not isinstance(serializeString,str):
            raise Exception("not str serializeString!")
        self.imgAnnos.clear()
        self.labels.clear()
        lines=serializeString.split("\n")
        for line in lines:
            #print(line)
            if not line:
                continue # line is empty
            if line.startswith(Check_header):
                continue
            if line.startswith(Label_line_header):
                self.setLabelsWithSerializeString(line)
                continue
            else:
                line_preprocess=line.split(":")
                print(line_preprocess)
                path_ls=[line_preprocess[0],line_preprocess[1]]
                path=":".join(path_ls)
                stringList=[path,line_preprocess[2]]
                self.updateAnnotationByString(stringList)
        #print(self.labels)
    def initEmpty(self):
        self.imgAnnos.clear()
        self.labels.clear()
        self.labels.append("__background__")
    def setLabelsWithSerializeString(self,labelSerializeString):
        if not isinstance(labelSerializeString,str):
            raise Exception("not str labelSerializeString!")
        self.labels.clear()
        labelStrings=labelSerializeString.split(",")
        labelDict={}
        for labelStr in labelStrings:
            if not labelStr:
                continue # labelStr is empty
            colonPos=labelStr.find(':')
            if colonPos<0:
                continue #skip no ID
            subLabel=labelStr.split(':')
            if subLabel[0]==0:
                continue
            labelDict[subLabel[0]]=subLabel[1]
        for value in labelDict.values():
            self.labels.append(value)
        self.labelChange.emit()
    def toSerializeString(self):
        labelSI=[]
        labelSI.append(Label_line_header)
        for i in range(len(self.labels)):
            if i == 0:
                continue
            str_SI="{}:{}".format(str(i),self.labels[i])
            labelSI.append(str_SI)
        print(labelSI)
        print(self.imgAnnos.items())
        allAnnoSI=[]
        for imageName,annos in self.imgAnnos.items():# const QMap<QString, Annotation> &annos = i.value();
            annoSI=[]
            for anno_name,anno in annos.items():
                str_anno="{0},{1},{2},{3},{4}".format(str(anno.labelId),str(anno.x1),str(anno.y1),
                                                      str(anno.x2),str(anno.y2))
                annoSI.append(str_anno)
            str_anno_all="{0}:{1}".format(imageName,",".join(annoSI))
            allAnnoSI.append(str_anno_all)
        print(allAnnoSI)
        return_str="{0}\n{1}".format(','.join(labelSI),'\n'.join(allAnnoSI))
        return return_str

    def addAnnotation(self,imageName,annotation,notify=True):
        if not isinstance(imageName,str) or not isinstance(annotation,Annotation):
            raise Exception("annotation type error!")
        if imageName not in self.imgAnnos:
            print(imageName)
            self.imgAnnos[imageName]={}
        if annotation.identStr() in self.imgAnnos[imageName]:
            return
        self.imgAnnos[imageName][annotation.identStr()]=annotation
        if notify:
            self.annotationChange.emit(imageName)


    def addAnnotationPara(self,imageName,id,x1,y1,x2,y2,notify=True):
        a=Annotation(id,x1,y1,x2,y2)
        print(a)
        self.addAnnotation(imageName,a,notify)

    def updateAnnotationByString(self,annotationStringList):
        if len(annotationStringList)<2:
            return
        imageName=annotationStringList[0]
        print(imageName)
        #print(imageName)
        #print(imageName)
        #print(self.imgAnnos)
        if not imageName in self.imgAnnos:
            print("update")
            self.imgAnnos[imageName]={}
        self.imgAnnos[imageName].clear()#this will add empty imagename
        subAnnotations=annotationStringList[1]
        #print(subAnnotations)
        sequence=subAnnotations.split(',')
        for i in range(0,len(sequence),5):
            if i + 5 >len(sequence):
                break
            id=int(float(sequence[i]))
            x1=int(float(sequence[i+1]))
            y1 = int(float(sequence[i + 2]))
            x2 = int(float(sequence[i + 3]))
            y2 = int(float(sequence[i + 4]))
            self.addAnnotationPara(imageName,id,x1,y1,x2,y2,False)
        self.annotationChange.emit(imageName)

    def removeAnnotation(self,imageName,key):
        if imageName in self.imgAnnos:
            #print("imageName:"+imageName)
            #print(self.imgAnnos[imageName].keys())
            if key.identStr() in self.imgAnnos[imageName]:
                self.imgAnnos[imageName].pop(key.identStr())
                #print(self.imgAnnos[imageName])
                self.annotationChange.emit(imageName)
    def clearAnnotationForImage(self,imageName):
        self.imgAnnos[imageName].clear()
        self.annotationChange.emit(imageName)
    def appendNewLabel(self,labelTxt):
        if len(self.labels)==0:
            self.labels.append("__background__")
        #labelTxt="Label-"+str(len(self.labels))
        self.labels.append(labelTxt)
        self.labelChange.emit()
    def getLabelText(self,labelid):
        if len(self.labels)>labelid:
            return self.labels[labelid]
        return ""
    def removeLabel(self,labelid):
        cnt=len(self.labels)
        if labelid <0 or labelid>self.userDefinedLabelCount():
            print("requested to remove non-existing labelID")
            return
        self.labels.remove(labelid)
        if cnt != len(self.labels):
            self.labelChange.emit()
    def userDefinedLabelCount(self):
        return len(self.labels)-1
    def getAnnotatedImageCount(self):
        return len(self.imgAnnos)
    def getAnnotationCountForImage(self,imageName):
        if not imageName in self.imgAnnos:
            return -1
        return len(self.imgAnnos[imageName])
    def getAnnotationsForImage(self,imageName):
        return self.imgAnnos[imageName].values()
    def getLabels(self):
        return self.labels
    def setLabelText(self,labelId,newLabel):
        if labelId>0 and len(self.labels)>labelId:
            self.labels[labelId]=newLabel
        self.labelChange.emit()


