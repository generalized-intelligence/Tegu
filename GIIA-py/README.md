![Tegu Logo](https://s2.ax1x.com/2019/01/30/kl6rzF.jpg)
# GIIA-Python
## Generalized Intelligence Image Annotator based on PyQt
## 泛化智能图像标注工具（Python版）

Tegu is a rapid development toolkit for non-ML programmers who need to use machine learning for some aspect of their work. From our development experience, most machine learning demands can be solved by very simple solutions, but most existing solutions are too heavy. For example, if a drone engineer needs to implement object recognition, it is not efficient for him to learning machine learning from scratch. Tegu is a light toolkit for Non-ML programmers to develop machine learning solutions. Tegu GUI supports Windows and Linux, providing the most common machine learning implementations. 

Also, for professional machine learning engineers, most of the work (such as parameter tuning) should be simplified. Tegu is a good set of tool to simplify the workflow.

---
泛化智能图像标注工具（ Generalized Intelligence Image Annotator，以下简称GIIA）是TeguCV 的一个配套工具，用于为计算机视觉方向的深度学习模型提供标注数据。该工具能以可视化的形式，帮助用户方便快捷地为深度学习模型准备经过标注的图像数据。该工具目前已在 Windows 10 1803 x64 平台测试通过。



## Quick Start

1. Install [Python3](https://www.python.org) and [pip3](https://pip.pypa.io/en/stable/installing)
2. Use the following command to install requirements:

```sh
pip3 install -r requirements.txt
```

3. Once all requirements are installed, use the following command to launch GIIA:
``` sh
python3 main.py
```
---

1. 首先请安装 [Python3](https://www.python.org) 以及 [pip3](https://pip.pypa.io/en/stable/installing)。
2. 使用如下命令安装所需的 Python 框架:

```sh
pip3 install -r requirements.txt
```

3. 安装好所需框架以后，使用以下命令运行 GIIA:
``` sh
python3 main.py
```


## File Structure

* config/: User Interface, written with [PyQt5](https://www.riverbankcomputing.com/software/pyqt/download5)
* Network/: Neural Networks, called by scripts in GUI/
* hook/: hook file used to make Windows .exe file
* Resource/: Elements used to make GUI
* Util/: Utility used in the project

---
* config/: 项目所需的一些配置所在位置
* UI_instance/: 项目的UI实例部分，使用 [PyQt5](https://www.riverbankcomputing.com/software/pyqt/download5) 编写。
* UI_instance/UI_model: 项目的UI定义和自定义控件部分，包含`*.ui`文件，可以使用 Qt Designer 配合 pyuic 修改并生成新的`*.py` UI定义文件。 
* model/: 项目中使用的工具组件、数据存储模型和自定义数据结构。
* main.py: 项目入口文件，同时还包括主窗体类的定义。


## Existing Features

* Video Classification (Long Video Classification)
* Image Recognition
* Facial Recognition (build feature library, and recognize)
* License Plate Recognition

HTTP API is available for Image Recognition, Facial Recognition and License Plate Recognition

---

* 读取文件夹中的文件，进行图片标注
* 支持同时添加多个文件夹
* 支持自定义多个标签
* 支持将未完成的标注储存为工程文件，工程文件(`*.json`)与标注文件(`*.serval`)将分开储存
* 对标注文件(`*.serval`)进行加密和解密——开源版GIIA使用的加密秘钥位于`config/defaults.py`中，默认设置为`GIIA-py-opensource`
* 将标注图像和标注文件打包成`*.zip`格式的压缩文件，便于上传——该功能依赖外部的`7z.exe`，位于`model/7zfiles`文件夹中

其中图像检测，人脸识别，车牌识别，都提供 HTTP API 可在使用时调用。

## User Manual

See [User Manual](http://www.giai.tech)

---

参见 [用户手册](http://www.giai.tech)

## Developer Document

See [User Manual](http://www.giai.tech)
---
参见 [开发者文档](http://www.giai.tech)


## TODO

* Optimization of interprocess communication
* Adding common neural networks, such as passenger detection, vehicle detection, and cat/dog detection
* Abnormality Detection in Restricted Zone (Training Free)
* Chinese NLP
* Hand Gesture Recognition, Pose Detection based on Feature Point Paring, Facial Feature Point Detection (Training Free)
* Image Segmentation
* General OCR
* Video Tracking (Work-In-Progress)

---

* 增加拆分`*.serval`文件到对应的图片文件夹功能
* 完整的多语言支持
* 集成压缩模块，不再依赖外部`7z`
* 对压缩打包功能添加多线程支持
* 在 macOS 和 Linux 平台上完成测试

# Meta

Project initialized by Generalized Intelligence

泛化智能 Generalized Intelligence 出品。

Distributed under the BSD 3-Clause license. See LICENSE for more information.

# Contribute

Please follow CONTRIBUTING.md

请参阅 CONTRIBUTING.md
