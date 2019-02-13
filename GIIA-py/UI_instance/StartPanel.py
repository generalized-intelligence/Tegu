from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from model.AnnotateImageModel import *
from UI_instance.UI_Model.Start import Ui_start
import model.EncryptTools as T
import config.defaults as DEF
class StartPanel(QWidget, Ui_start):
    recent_loaded=pyqtSignal()
    def __init__(self,Aim:AnnotatedImageModel,recent_dict:dict ,parent=None):
        super(StartPanel, self).__init__(parent)
        self.setupUi(self)
        self.aim=Aim
        self.recent_dict=recent_dict
        print(self.recent_dict)
        self.list_projname=list(self.recent_dict.keys())
        self.list_model=QStringListModel(self.list_projname)
        self.listRecent.setModel(self.list_model)
        self.picture_path=[]
        self.listRecent.doubleClicked.connect(self.load_recent_by_index)
    def load_recent_by_index(self,index:QModelIndex):
        row=index.row()
        proj_name=self.list_projname[row]
        serval_path=self.recent_dict[proj_name]['serval']
        proj_path=self.recent_dict[proj_name]['proj']
        #print(proj_path)
        import os
        if not os.path.exists(proj_path):
            QMessageBox.warning(self, "打开工程失败", "工程文件不存在:" + proj_path, QMessageBox.Ok)
            return
        else:
            result=self.OpenProjFileWithName(proj_path)
            if result:
                if os.path.exists(serval_path):
                    result_serval=self.OpenServalFileWithName(serval_path)
                    if not result_serval:
                        QMessageBox.warning(self, "未能打开标注文件", "工程将以无标注开始", QMessageBox.Ok)
                else:
                    QMessageBox.warning(self, "没有找到标注文件", "工程将以无标注开始", QMessageBox.Ok)
            else:
                #QMessageBox.warning(self, "打开工程失败", "工程文件不合法:" + proj_path, QMessageBox.Ok)
                return
        self.recent_loaded.emit()



    def OpenServalFileWithName(self,file_path:str):
        try:
            with open(file_path, encoding='utf-8') as f:
                file_read = f.read()
        except Exception as e:
            QMessageBox.warning(self, "打开文件失败", "无法打开文件:" + file_path, QMessageBox.Ok)
            return False
        serval_content = T.decrypt(DEF.ENCRYPT_KEY, file_read)
        # print(serval_content)
        if T.validateHeader(serval_content) != 0:
            QMessageBox.warning(self, "校验失败", "不是合法的标注文件:" + file_path, QMessageBox.Ok)
            return False
        self.aim.initWithSerializeString(serval_content)
        # print(self.aim.imgAnnos)
        return True

    def OpenProjFileWithName(self,file_path:str):
        import json
        try:
            with open(file_path, encoding='utf-8') as f:
                proj_dict = json.loads(f.read())
            #print(proj_dict)
            if 'images' in proj_dict.keys() and 'labels' in proj_dict.keys():
                self.picture_path = proj_dict['images']
                self.aim.labels = proj_dict['labels']
                self.load_proj = True
            QMessageBox.information(self, "打开完成", "已载入工程:" + file_path, QMessageBox.Ok)
            return True
        except Exception as e:
            QMessageBox.warning(self, "打开文件失败", "无法打开文件:" + file_path, QMessageBox.Ok)
            return False


