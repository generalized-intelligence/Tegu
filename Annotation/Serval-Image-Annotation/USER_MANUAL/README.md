![Tegu Logo](https://s2.ax1x.com/2019/01/30/kl6rzF.jpg)
# GIIA-Python
## Generalized Intelligence Image Annotator based on PyQt
## 泛化智能图像标注工具（Python版）用户手册

### 概述
泛化智能图像标注工具（ Generalized Intelligence Image Annotator，以下简称GIIA）是TeguCV 的一个配套工具，用于为计算机视觉方向的深度学习模型提供标注数据。该工具能以可视化的形式，帮助用户方便快捷地为深度学习模型准备经过标注的图像数据。该工具目前已在 Windows 10 1803 x64 平台测试通过，，理论上可以直接在Linux和macOS平台上运行（未经测试）。

本软件要求屏幕分辨率不小于 1024X768 。
---
Tegu Image Annotator(TIA) is a tool which works with TeguCV. The TIA is used to provide annotated data for the deep learning models in computer vision. It can help user to annotate image data fast and easily.

The TIA has been tested on Windows 10 1803 x64 platform, and also provides support of the Linux and macOS platforms (not tested).

The TIA requires that your screen resolution is not smaller than 1024 X 768
---


### 功能

* 读取文件夹中的文件，进行图片标注
* 支持同时添加多个文件夹
* 支持自定义多个标签
* 支持将未完成的标注储存为工程文件，工程文件(`*.json`)与标注文件(`*.serval`)将分开储存
* 对标注文件(`*.serval`)进行加密和解密——开源版GIIA使用的加密秘钥位于`config/defaults.py`中，默认设置为`GIIA-py-opensource`
* 将标注图像和标注文件打包成`*.zip`格式的压缩文件，便于上传——该功能依赖外部的`7z.exe`，位于`model/7zfiles`文件夹中

---
* Read and annotate image files in folders
* Add multiple folders
* Customize multiple labels
* Save your imcomplete annotating project as files , project files(`*.json`) and annotation files(`*.serval`) will be storaged seperately
* Encrypt and decrypt annotation files(`*.serval`).The Encryption key of the TIA open-source version is located in `config/defaults.py`, set as `TIA-py-opensource`
* Compress image files and annotation files in a zip file`*.7z`,which relies on an outer executable file `7z.exe`, located in `model/7zfiles`

---


### 使用说明
#### 新建项目
软件启动之后，主界面如图所示：

---
When the TIA launches, the main window shows as follow:
![main](https://raw.githubusercontent.com/generalized-intelligence/Tegu/master/Annotation/Serval-Image-Annotation/USER_MANUAL/resources/main.png)


下方白色区域将显示最近打开的项目（如果有），若想打开这些项目，直接双击对应项即可。点击“新建项目”按钮，即可建立新的项目。
---
The following spaces shows the recent projects(if there are), if you want to open the project, just double click the item. Click "New Project" to create a new project.

![newproj](https://raw.githubusercontent.com/generalized-intelligence/Tegu/master/Annotation/Serval-Image-Annotation/USER_MANUAL/resources/newproj.png)

点击“添加图片路径”按钮，可以添加一个文件夹中的所有图片到工作区中——软件会递归搜索该文件夹的所有子文件夹。侧面将显示当前已找到的图片总数。
---
Click "Add picture path" to add all the pictures in a folder to the project. The TIA will search recurcively all those subfolders. At the right of the window shows the total number of the pictures got.
![addfolder](https://raw.githubusercontent.com/generalized-intelligence/Tegu/master/Annotation/Serval-Image-Annotation/USER_MANUAL/resources/addfolder.png)

下方区域是标签区，点击“添加标签”即可增加一个新的标签，标签默认以`Label-X`命名，用户可以根据需要，直接自行修改标签的名字。
---
The following spaces is label zone, click "Add label" to add a new label named as `Label-X`, you can change the label name if necessary.
![addlabel](https://raw.githubusercontent.com/generalized-intelligence/Tegu/master/Annotation/Serval-Image-Annotation/USER_MANUAL/resources/addlabel.png)

若要删除已有标签，可点击对应标签的数字，选中要删除的标签，然后点击下方的“删除标签”按钮。
---
Click the label number and then click "Delete label" to remove the label.

#### 标注界面
在添加完图片和标签之后，即可点击“开始标注”按钮，进入标注工作区。注意**开始标注之前必须添加图片和标签**。工作区主界面如下图所示：
---
After adding pictures and labels, click "Start Annotation" to enter the annotation workspace. Notice that **you must add pictures and labels before annotation**. The workspace shows as follows:

![workspace](https://raw.githubusercontent.com/generalized-intelligence/Tegu/master/Annotation/Serval-Image-Annotation/USER_MANUAL/resources/workspace.png)

为了方便用户使用，软件提供了一些针对各个功能的快捷键，右侧“快捷键”选项卡显示了这些快捷键的具体内容。
---
To improve the efficency, the TIA provides some key shortcuts for those annotation functions, click the "key shortcuts" tab to show those keymap.

左侧界面显示用户图片的具体内容——点击下方的`+`和`-`按钮，可以放大或缩小图片，点击正中央的`1:1`按钮，可以让图片恢复原始显示尺寸。
---
The left space shows the current picture, click the `+` and `-` button below the picture to zoom in or zoom out the picture, and click the `1:1` button to recover the picture into original size.

下方文本框会显示当前标注区域的对角坐标和鼠标指针当前的坐标，可供参考。
---
The textbox under the picture shows the diagonal coordinates of current annotation zone and the coordinate of the mouse cursor as a referrence.

点击右侧界面的“项目资源”选项卡，可以显示当前加载的所有图片（此处显示绝对路径）。在指定图片上双击可跳转至指定图片。若需要选择下一张或上一张图片，点击“下一张”`Next`或“上一张”`Prev`按钮即可。
---
Click the "project resources" tab to show all those absolute paths of the pictures in current project. Double click to open the picture , click `Next` or `Prev` to go to the next or previous picture. 

界面中间位置列举了此前添加的所有标签，点击最上方的“跳过”`Skip`按钮可以跳过当前图片。
---
The middle area of the workspace shows all the labels added, click the `Skip` button to skip the current picture.

#### 开始进行标注
在需要标注的图片上，点击界面中间位置的对应标签的按钮，即可切换到标注状态。将鼠标移动到工作区，在要进行标注的区域拖拽，即可新建一个标注区：
---
Click the button of the label you want to annotate, then you'll get into annotating state. Move your mouse to the workspace and drag to create a new annotation zone.
![annotating](https://raw.githubusercontent.com/generalized-intelligence/Tegu/master/Annotation/Serval-Image-Annotation/USER_MANUAL/resources/annotating.png)

若需要更改某一个标注区的位置，可以直接使用鼠标对其进行拖拽。点击某个标注区，拖拽其周围的黑色控制块，可以改变它的大小。
---
You can directly drag an annotation zone to move it, and drag the black control blocks to change its size.
![adjust](https://raw.githubusercontent.com/generalized-intelligence/Tegu/master/Annotation/Serval-Image-Annotation/USER_MANUAL/resources/adjust.png)

若想要删除某一个标注区，可以点击右侧的“删除”`Delete`键，即可进入删除模式。此时图片上的所有标注区右上角都会多出一个叉号按钮。点击该按钮，即可删除对应的标注区。
---
Click "Delete" button to enter the deleting mode, then all those annotation zones on the picture will show a cross button on the right corner, click the button to delete the annotation zone.
![delete](https://raw.githubusercontent.com/generalized-intelligence/Tegu/master/Annotation/Serval-Image-Annotation/USER_MANUAL/resources/delete.png)

若想跳过当前图片，可以点击上方的“跳过”`Skip`按钮，此时该图片的所有标注区都将被清空，效果如下所示：
---
Click "Skip" to skip current picture, then all the annotation zones will be cleaned up as follows:
![skip](https://raw.githubusercontent.com/generalized-intelligence/Tegu/master/Annotation/Serval-Image-Annotation/USER_MANUAL/resources/skip.png)

点击“保存”`Save`按钮，可以保存到指定的`*.serval`文件中。此外也可以指定保存`*.json`工程文件。工程文件中只包括图片文件夹和标签的信息，不包括标注数据。
---
Click "save" button to save annotation information to the specific `*.serval` files. You can also save your project to the project files `*.json`. The project files contain the information of picture paths and labels, which **do not** contain the information of annotation zones.
//产品逻辑是否修改？
#### 打开已有的工程
在主界面点击“打开项目文件”按钮，可以选择加载已有的`*.json`项目文件。若已有`*.serval`文件，则可以一并加载。完成加载之后即可恢复此前已有的所有文件、标签和标注信息。
---
Click "open project file" button to load the project file `*.json`, you can also load annotation file `*.serval` if you have got one. The previous files, labels and annotations will be recovered after project loaded.

#### 将标注数据打包
若需要标注数据具有可移动性，则可以对标注数据进行打包，将图片文件和标注文件打包进一个`*.7z`文件中。在主界面点击“打包”即可进入打包上传界面。
---
You need to pack your annotation datas to make your datas portable, the packing function will create a `*.7z` file which contains picture files and annotation file. Click "Pack" to enter the packing workspace.

![upload](https://raw.githubusercontent.com/generalized-intelligence/Tegu/master/Annotation/Serval-Image-Annotation/USER_MANUAL/resources/upload.png)

- 点击“选择Serval文件”按钮，可以载入一个标注文件。软件将自动搜索标注文件中标注的所有图片文件，请**确保这些文件没有被移动或删除**。
- 点击“选择7z程序位置”按钮，选择调用外部的`7z.exe`的位置。本项目自带的`7z.exe`文件在`model/7zfiles`目录下。
- 点击“选择保存文件位置”按钮，选择保存压缩包的位置。
---
- Click "Select Serval file" button to load a serval file, the TIA will search all the picture files in the serval file, please **make sure all those files are not moved or deleted.**
- Click "Select 7z file" to choose which `7z.exe` to call, the `7z.exe` in the TIA folder is located in `model/7zfiles` folder.
- Click "Selct save path" to select where to save the packed file.
![added](https://raw.githubusercontent.com/generalized-intelligence/Tegu/master/Annotation/Serval-Image-Annotation/USER_MANUAL/resources/added.png)

- 最后，点击“打包”即可开始进行打包。若图片文件较多，则会需要比较长的时间，请耐心等待，并确保打包文件保存的位置有足够的存储空间。
---
- Finally click "Pack" to start packing, it will take a long time if you have got many picture files , please wait patiently and make sure there is enough free space.

打包完成之后如下图所示：
---
The file structure of the packed file shows as follow:
![packdone](https://raw.githubusercontent.com/generalized-intelligence/Tegu/master/Annotation/Serval-Image-Annotation/USER_MANUAL/resources/packdone.png)

#### 标注文件和打包文件结构说明
软件默认会对`*.serval`文件进行加密，若您不想对文件加密，您可以修改`config/defaults.py`，修改以下代码：
---
The TIA will defaultly encrypt the `*.serval` file, if you don't want to encrypt the file, you can modify the file `config/defaults.py`, the following part:
```python
ENCRYPT_KEY="GIIA-py-opensource"
```
为：
---
as:
```python
ENCRYPT_KEY=""
```

一个解密后的文件格式如下所示：
---
Here is the structure of a decrypted serval file:
```
aimg0000825a7dd7ab6fc10f270e8b9dfa4f5a96
0:__background__,1:Label-1,2:Label-2,3:Label-3,4:Label-4
C:/Users/qrato/Pictures/Saved Pictures/std_pic.jpg:1,518,288,833,624,2,1106,584,1328,837
C:/Users/qrato/Pictures/Saved Pictures/tempfile.jpg:3,568,342,903,541
C:/Users/qrato/Pictures/Saved Pictures/test.jpg:4,1205,514,1727,950
```
第一行为完整性校验码，第二行为标签（其中`0:__background__`为背景），接下来每一行都是对应的文件和标注区域（标签，对角点坐标）。此处储存的文件路径均为绝对路径，因此若您直接使用`*.serval`文件在本机执行训练，请**务必确保您的图片文件没有被移动或删除**。
---
Line 1 is the checksum code, line 2 is the labels line(`0:__background__`as background), and the following lines are the picture files and the annotation zones(label,diagonal coordinates). The file paths here are all full paths, if you want to use the serval file directly to train local, please **make sure all your picture files are not moved or deleted.**
---
若要将数据文件传输至另一台训练用机（例如泛化智能提供的服务器），您需要使用打包功能将文件打包。打包完成之后的压缩包结构如下所示：
---
You need to pack the training data if you want to transfer your data to another trainer (e.g. the server of GIAI.tech). The zipped file structure shows as follow:

![unzip](https://raw.githubusercontent.com/generalized-intelligence/Tegu/master/Annotation/Serval-Image-Annotation/USER_MANUAL/resources/unzip.png)

经过解密的`serval`文件如下所示：
---
The serval file decrypted shows as follow:
```
aimg00006ace52691f26af037438575c47123c44
0:__background__,1:Label-1,2:Label-2,3:Label-3,4:Label-4
C_Users_qrato_Pictures_Saved Pictures/std_pic.jpg:1,518,288,833,624,2,1106,584,1328,837
C_Users_qrato_Pictures_Saved Pictures/tempfile.jpg:3,568,342,903,541
C_Users_qrato_Pictures_Saved Pictures/test.jpg:4,1205,514,1727,950
```
此时储存的文件路径为相对路径，您可以安全地将整个压缩包转移至目标机。
---
Now all the filepaths are relative paths, you can move the data to the target PC safety.






