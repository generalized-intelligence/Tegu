from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QMessageBox,QFileDialog,QListWidgetItem
from model.AnnotateImageModel import *
from UI_instance.UI_Model.Config import Ui_config
from config.defaults import *
class ConfigPane(QWidget, Ui_config):
    """
    Class documentation goes here.
    """
    ConfigStartAnnotation=pyqtSignal()
    annotationModeChange=pyqtSignal(int)
    def __init__(self,aim:AnnotatedImageModel, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(ConfigPane, self).__init__(parent)
        self.setupUi(self)
        self.folder_list=[]
        self.picture_path=[]
        self.proj_name="新项目"
        self.txtProjname.setText(self.proj_name)
        self.btnAdd.clicked.connect(self.add_folder)
        self.pic_num=0
        self.aim=aim
        self.action_list.setupButtons(self.btnLabelAdd,self.btnLabelDel,self.btnStart)
        self.action_list.startAnnotation.connect(self.StartingAnno)
    def search_pic(self,dir_path):
        import os
        sub_path=os.listdir(dir_path)
        for item in sub_path:
            new_path=dir_path+'/'+item
            if os.path.isdir(new_path) and new_path not in self.folder_list:
                self.folder_list.append(new_path)
                new_path_item = QListWidgetItem()
                new_path_item.setText(new_path)
                self.listWidget.addItem(new_path_item)
                print(new_path)
                self.search_pic(new_path)
            elif os.path.splitext(item)[1].lower().replace('.','') in SUPPORTED_FILE_FORMATS_LIST:
                self.pic_num+=1
                self.picture_path.append(new_path)
        print(self.picture_path)
    def add_folder(self):
        dir_path = QFileDialog.getExistingDirectory(self, "选择图片所在目录", "C:/Users")
        print(dir_path)
        if dir_path not in self.folder_list:
            self.folder_list.append(dir_path)
            dir_path_item=QListWidgetItem()
            dir_path_item.setText(dir_path)
            self.listWidget.addItem(dir_path_item)
            self.search_pic(dir_path)
            self.lblstatus.setText("已选定"+str(self.pic_num)+"个图片")
            print("当前已选定"+str(self.pic_num)+"个图片")
    def StartingAnno(self):
        print("starting annotations")
        actionItems=self.action_list.action_items
        userAction=self.action_list.user_actions
        self.proj_name=self.txtProjname.text()
        print(actionItems)
        print(userAction)
        for k,v in userAction.items():
            print(k,v)
            self.aim.appendNewLabel(v.action_label)
        print(self.aim.labels)
        self.ConfigStartAnnotation.emit()







