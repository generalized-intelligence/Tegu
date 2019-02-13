from PyQt5.QtCore import pyqtSlot, Qt,QTranslator
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QListWidgetItem, QMessageBox,QStackedWidget,QFileDialog
from PyQt5.QtGui import QPixmap
from UI_instance.UI_Model.MainWindow import Ui_MainWindow
from model.AnnotateImageModel import *
import model.EncryptTools as T
import config.defaults as DEF
from UI_instance.ConfigPane import ConfigPane
from UI_instance.AnnotatorPane import AnnotatorPane
from UI_instance.StartPanel import StartPanel
from UI_instance.ZipPanel import *
import cgitb
cgitb.enable( format ='text')

class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow,self).__init__()
        self.aim=AnnotatedImageModel()
        self.recent_dict = {}
        self.json_load()
        self.configPane=ConfigPane(self.aim)
        self.annoPane=AnnotatorPane(self.aim)
        self.start=StartPanel(self.aim, self.recent_dict)
        self.zipPanel=ZipPanel()
        self.setupUi(self)
        self.trans=QTranslator()
        self.initUi()
        self.configPane.ConfigStartAnnotation.connect(self.startAnnotationRequested)
        self.configPane.returnBtn.clicked.connect(self.returnMain)
        self.annoPane.pushButtonSave.clicked.connect(self.SaveAll)
        self.annoPane.endAnnotation.connect(self.exitApplication)
        self.start.button_new.clicked.connect(self.newProj)
        self.start.button_open.clicked.connect(self.OpenAll)
        self.start.button_pack.clicked.connect(self.startZip)
        self.picture_path=[]
        self.proj_name=""
        self.load_proj=False

    def json_load(self):
        import os
        import json
        if os.path.exists(DEF.RECENT_JSON):
            with open(DEF.RECENT_JSON,'r',encoding='utf-8') as f:
                self.recent_dict=json.loads(f.read())
    def json_dump(self):
        import json
        with open(DEF.RECENT_JSON,'w',encoding='utf-8') as f:
            f.write(json.dumps(self.recent_dict))
    def initUi(self):
        self.stack.addWidget(self.start)
        self.stack.addWidget(self.configPane)
        self.stack.addWidget(self.annoPane)
        self.stack.addWidget(self.zipPanel)
        self.stack.setCurrentWidget(self.start)
        self.setCentralWidget(self.stack)
        #self.configPane.action_list.startAnnotation.connect(self.startAnnotationRequested)
    def startZip(self):
        self.stack.setCurrentWidget(self.zipPanel)
    def returnMain(self):
        self.stack.setCurrentWidget(self.start)
    def startAnnotationRequested(self):
        if not self.load_proj:
            self.picture_path = self.configPane.picture_path
            self.proj_name=self.configPane.proj_name
        if len(self.picture_path)<1:
            print(self.picture_path)
            QMessageBox.information(self,"提示","没有选择图片！请重新选择",QMessageBox.Ok)
            return
        if len(self.aim.labels)<1:
            QMessageBox.information(self, "提示", "没有添加标签！请重新选择", QMessageBox.Ok)
            return

        self.annoPane.setImageFileList(self.picture_path)
        self.annoPane.updateLabels()
        self.stack.setCurrentWidget(self.annoPane)
        self.annoPane.loadFirstImage()
    def exitApplication(self):
        reply = QMessageBox.question(self, ("确认退出"),
                                      ("是否要退出程序？未保存的进度都将丢失"),QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.exit();
    def OpenServalFile(self):
        file_path_diag=QFileDialog.getOpenFileName(self, "打开文件", "C:/Users/",
                                                "serval files (*.serval);;all files(*.*)")
        file_path=file_path_diag[0]
        print(file_path)
        try:
            with open(file_path,encoding='utf-8') as f:
                file_read=f.read()
        except Exception as e:
            QMessageBox.warning(self, "打开文件失败", "无法打开文件:" + file_path, QMessageBox.Ok)
            return False
        serval_content=T.decrypt(DEF.ENCRYPT_KEY,file_read)
        print(serval_content)
        if T.validateHeader(serval_content)!=0:
            QMessageBox.warning(self, "校验失败", "不是合法的标注文件:" + file_path, QMessageBox.Ok)
            return False
        self.aim.initWithSerializeString(serval_content)
        print(self.aim.imgAnnos)
        return True
    def newProj(self):
        self.stack.setCurrentWidget(self.configPane)
    def SaveAll(self):
        if self.SaveServalFile():
            reply = QMessageBox.question(self, ("是否保存工程文件"),
                                         ("工程文件仅包含文件列表和标签，便于继续下一次标注"), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply==QMessageBox.Yes:
                if self.SaveProjFile():
                    self.json_dump()
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False
    def OpenAll(self):
        proj=self.OpenProjFile()
        if proj:
            reply = QMessageBox.question(self, ("是否打开标签文件"),
                                         ("若有标签文件则可以加载已标注的结果"), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                serval=self.OpenServalFile()
            self.startAnnotationRequested()

    def OpenProjFile(self):
        import json
        #proj_dict = {'images': self.picture_path, 'labels': self.aim.getLabels()}
        file_path_diag = QFileDialog.getOpenFileName(self, "打开工程文件", "C:/Users/",
                                                     "json files (*.json);;all files(*.*)")
        file_path = file_path_diag[0]
        try:
            with open(file_path,encoding='utf-8') as f:
                proj_dict=json.loads(f.read())
            if 'images' in proj_dict.keys() and 'labels' in proj_dict.keys():
                print(proj_dict)
                self.picture_path=proj_dict['images']
                self.aim.labels=proj_dict['labels']
                self.load_proj = True
            QMessageBox.information(self, "打开完成", "已载入工程:" + file_path, QMessageBox.Ok)
            return True
        except Exception as e:
            QMessageBox.warning(self, "打开文件失败", "无法打开文件:" + file_path, QMessageBox.Ok)
            return False
    def SaveProjFile(self):
        import json
        proj_dict={'images':self.picture_path,'labels':self.aim.getLabels()}
        file_path_diag = QFileDialog.getSaveFileName(self, "保存工程文件", "C:/Users/"+self.proj_name,
                                                     "json files (*.json);;all files(*.*)")
        file_path = file_path_diag[0]
        try:
            file_save=open(file_path,'w',encoding="utf-8")
            data_to_write = json.dumps(proj_dict)
            file_save.write(data_to_write)
            file_save.close()
            self.recent_dict[self.proj_name]['proj']=file_path
            QMessageBox.information(self,"保存完成","文件已保存到:"+file_path,QMessageBox.Ok)
            return True
        except Exception as e:
            QMessageBox.warning(self, "保存文件失败", "无法打开文件:" + file_path, QMessageBox.Ok)
            return False

    def SaveServalFile(self):
        file_path_diag = QFileDialog.getSaveFileName(self, "保存标注文件", "C:/Users/"+self.proj_name,
                                                "serval files (*.serval);;all files(*.*)")
        #print(file_path)
        file_path=file_path_diag[0]
        try:
            file_save=open(file_path,'w',encoding="utf-8")
            data_to_write = T.addHeader(self.aim.toSerializeString())
            print(data_to_write)
            data_encrypt=T.encrypt(DEF.ENCRYPT_KEY,data_to_write)
            file_save.write(data_encrypt)
            file_save.close()
            self.recent_dict[self.proj_name]={'serval':file_path}
            QMessageBox.information(self,"保存完成","文件已保存到:"+file_path,QMessageBox.Ok)
            return True
        except Exception as e:
            QMessageBox.warning(self, "保存文件失败", "无法打开文件:" + file_path, QMessageBox.Ok)
            return False



if __name__ == "__main__":
    app = QApplication(sys.argv)
    qshow = MainWindow()
    qshow.show()
    sys.exit(app.exec_())