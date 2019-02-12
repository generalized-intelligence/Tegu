from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from model.ZipUtil import *
from config import defaults as DEF
from UI_instance.UI_Model.ZipPanel import Ui_zippanel
import os
class ZipPanel(QWidget,Ui_zippanel):
    updatingTxtDisplay=pyqtSignal()
    def __init__(self,parent=None):
        super(ZipPanel, self).__init__(parent)
        self.setupUi(self)
        self.serval_dict={}
        self.txt_display="本功能需要使用7z，请指定正确的7z.exe位置\n"
        self.ziptool_Path=""
        self.zip_Path=""
        self.btnServal.clicked.connect(self.select_serval)
        self.btnZipTool.clicked.connect(self.select_zip)
        self.updatingTxtDisplay.connect(self.updateTxtDisplay)
        self.btnSave.clicked.connect(self.select_save)
        self.btnStart.clicked.connect(self.zip_pack)
        self.updatingTxtDisplay.emit()
    def select_save(self):
        file_path_diag = QFileDialog.getSaveFileName(self, "保存文件", "C:/Users/",
                                                     "7z files (*.7z);;all files(*.*)")
        file_path = file_path_diag[0]
        if file_path != "":
            self.zip_Path = file_path
            self.txt_display += "将保存到以下位置：" + file_path + '\n'
            self.updatingTxtDisplay.emit()
    def zip_pack(self):
        if self.zip_Path=="":
            QMessageBox.warning(self, "无法打包", "请先选择保存位置！" , QMessageBox.Ok)
            return
        elif self.ziptool_Path=="":
            QMessageBox.warning(self, "无法打包", "请先选择7z.exe程序位置！", QMessageBox.Ok)
            return
        elif len(self.serval_dict.keys())<=1:
            QMessageBox.warning(self, "无法打包", "请先打开有效的serval文件！", QMessageBox.Ok)
            return
        ZP = Ziputil(self.ziptool_Path, self.zip_Path)
        temp_path=os.path.splitext(self.zip_Path)[0]+"_folder"
        self.txt_display += "正在复制文件，操作时间可能较长，请耐心等待"  + '\n'
        self.updatingTxtDisplay.emit()
        ls=write_folder_from_dict(temp_path,self.serval_dict)
        if len(ls)==0:
            self.txt_display += "复制完成" + '\n'
        else:
            self.txt_display+="以下文件没有找到：\n"
            for item in ls:
                self.txt_display+=item
                self.txt_display+='\n'
        self.updatingTxtDisplay.emit()
        self.txt_display += "正在执行压缩，操作时间可能较长，请耐心等待" + '\n'
        self.updatingTxtDisplay.emit()
        code = ZP.genzipfile(temp_path)
        if code==0:
            self.txt_display += "压缩完成，文件已保存到："+self.zip_Path + '\n'
            self.updatingTxtDisplay.emit()
        else:
            self.txt_display += "压缩出错，请确保7z.exe正常工作" +  '\n'
            self.updatingTxtDisplay.emit()

    def updateTxtDisplay(self):
        self.txtOut.setPlainText(self.txt_display)
    def select_serval(self):
        file_path_diag = QFileDialog.getOpenFileName(self, "打开文件", "C:/Users/",
                                                     "serval files (*.serval);;all files(*.*)")
        file_path = file_path_diag[0]
        print(file_path)
        try:
            with open(file_path, encoding='utf-8') as f:
                file_read = f.read()
        except Exception as e:
            QMessageBox.warning(self, "打开文件失败", "无法打开文件:" + file_path, QMessageBox.Ok)
            return False
        serval_decrypt=decrypt(DEF.ENCRYPT_KEY,file_read)
        if validateHeader(serval_decrypt)!=0:
            QMessageBox.warning(self, "文件校验失败", "以下文件不是合法的serval文件:" + file_path, QMessageBox.Ok)
            return False
        self.serval_dict=load_serval(decrypt(DEF.ENCRYPT_KEY,file_read))
        self.txt_display+="已打开serval文件："+file_path+'\n'
        self.txt_display += "将打包以下文件：" +'\n'
        for key in self.serval_dict.keys():
            if key != 'label_line':
                path = self.serval_dict[key]['path']
                full_pic = path + '/' + key
                self.txt_display+=(full_pic+'\n')
        self.updatingTxtDisplay.emit()
        return True
    def select_zip(self):
        file_path_diag = QFileDialog.getOpenFileName(self, "打开文件", "C:/Users/",
                                                     "exe files (*.exe);;all files(*.*)")
        file_path = file_path_diag[0]
        if file_path!="":
            self.ziptool_Path=file_path
            self.txt_display+="将使用以下位置的7z工具："+file_path+'\n'
            self.updatingTxtDisplay.emit()



