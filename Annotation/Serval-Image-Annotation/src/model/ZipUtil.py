import shutil
from model.EncryptTools import *
from config import defaults as DEF
ZIP_PASS=DEF.ZIP_PASS
import os
class Ziputil():
    def __init__(self, ziptoolpath:str, zipfilepath:str):
        self.ziptoolpath=ziptoolpath
        self.zipfilepath=zipfilepath
        self.password=ZIP_PASS
    def getzipfile(self):
        with open('blankfile','w') as f:
            f.write('\n')
        command=' a '+self.zipfilepath+' '+os.getcwd()+'\\blankfile -p'+ZIP_PASS
        print(self.ziptoolpath+command)
        code=os.system(self.ziptoolpath+command)
        return code
    def genzipfile(self,folder_path:str):
        command=" a -t7z -scsUTF-8 "+self.zipfilepath+" "+folder_path+"\\* -p"+ZIP_PASS
        print(self.ziptoolpath+command)
        code = os.system(self.ziptoolpath + command)
        return code


def load_serval(str_serval:str):
    lines=str_serval.split('\n')
    serval_dict={}
    for line in lines:
        if line.startswith('aimg'):
            continue
        if line.startswith('0:__background__'):
            serval_dict['label_line']=line
            continue
        line_split=line.split(':')
        line_path_full=':'.join([line_split[0],line_split[1]])
        print(line_path_full)
        line_path_full_split=line_path_full.split('/')
        path_folder='/'.join(line_path_full_split[:-1])
        file_name=line_path_full_split[-1:][0]

        anno_str=line_split[2]
        serval_dict[file_name]={'path':path_folder,'anno':anno_str}
    return serval_dict
def get_path_folder(path):
    path_folder = '_'.join(path.split('/'))
    return path_folder.replace(':','')
def regenerate_serval(serval_dict:dict):
    list_to_write=[]
    list_to_write.append(serval_dict['label_line'])
    for key in serval_dict.keys():
        if key!='label_line':
            path=serval_dict[key]['path']
            anno=serval_dict[key]['anno']
            str_line=get_path_folder(path)+'/'+key+':'+anno
            list_to_write.append(str_line)
    serval_new='\n'.join(list_to_write)
    serval_new_header=addHeader(serval_new)
    return serval_new_header
def write_folder_from_dict(path:str, serval_dict:dict):
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)
    os.chdir(path)
    with open('encrypt_serval.serval','w',encoding='utf-8') as f:
        f.write(encrypt(DEF.ENCRYPT_KEY,regenerate_serval(serval_dict)))
    fail_list=[]
    for key in serval_dict.keys():
        if key!='label_line':
            path = serval_dict[key]['path']
            full_pic =path+'/'+key
            try:
                new_path = get_path_folder(path)
                if not os.path.isdir(new_path):
                    os.mkdir(new_path)
                shutil.copy(full_pic,new_path)
            except Exception as e:
                print(e)
                fail_list.append(key)
    return fail_list


if __name__=="__main__":
    with open('zip.serval',encoding='utf-8') as f:
        str_serval=f.read()
    #with open('decrypt.serval','w',encoding='utf-8') as f_write:
    #    f_write.write(decrypt(ENCRYPT_KEY,str_serval))
    serval_dict=load_serval(decrypt(DEF.ENCRYPT_KEY,str_serval))
    #print(serval_dict)
    #print(serval_dict['label_line'])
    import os
    ls=write_folder_from_dict(os.getcwd(), serval_dict)
    print(ls)
    #import os
    os.chdir('../')
    print(os.getcwd())

    ZP=Ziputil(os.getcwd()+'\\7zfiles\\7z.exe',os.getcwd()+'\\zipdemo.7z')
    code=ZP.genzipfile('"'+os.getcwd()+'\\writing_path"')
    print(code)

