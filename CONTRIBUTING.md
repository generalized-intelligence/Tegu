# Roadmap

Tegu is a rapid development toolkit, designed for non-ML programmers to develop machine learning enabled solutions. Therefore, the GUI component of the toolkit is crucial. We would like to simplify the training process to the greatest extent. In some case, we even provide training-free solutions for machine learning tasks. With HTTP protocols, users do not need to use any machine learning related programming. Any languages that are compatible with HTTP protocols can be used to communicate with Tegu.

The project is consist of two parts: Network and GUI.

Network: this part currently has implementations in image recognition, video classification, facial recognition, and license plate recognition.

GUI: this part contains the GUI for existing networks and HTTP API.

We would like to cover as many use cases as possible, so one of the major goals is to add a variety of neural networks to fulfill demands in different use cases.

---

Tegu 是一个为非专业机器学习工程师设计的开源机器学习快速开发工具。 在 Tegu 中会需要 GUI 组件的参与。 我们希望提供一个尽量简化训练， 甚至免训练的方式来满足大多数机器学习任务。借助 HTTP 通信的形式，用户更加容易的使用 Tegu 的同时，不需要学习任何有关代码。任何能够使用 HTTP 通信的语言都可以与 Tegu 对接.

这个项目分为网络部分以及 GUI 部分。

网络部分，目前包含了图像检测，视频分类，人脸检测，以及车牌检测，四种不同的应用场景。

GUI 部分，包含使用 GUI 操作网络的所有功能，及 HTTP API 功能。

我们希望能够覆盖更多的应用场景， 所以项目很大的一个目标是添加更多类型的网络满足各种应用场景。

# Contributing

1. We welcome and appreciate all contributions toward any one of the following topics:

* Optimization of interprocess communication
* Adding common neural networks, such as passenger detection, vehicle detection, and cat/dog detection
* Abnormality Detection in Restricted Zone (Training Free)
* Chinese NLP
* OCR for common documents, such as personal identifications or receipts (Training Free)
* Hand Gesture Recognition, Pose Detection based on Feature Point Paring, Facial Feature Point Detection (Training Free)
* Image Segmentation
* General OCR
* Video Tracking (Work-In-Progress)

2. If you would like to contribute towards a feature that is not listed in the To-do list, please try to explain why you think the feature is important for Tegu. A real-life use case of such feature would be a great way to let us know what you think of the feature. We will review each new feature based on the usability of the feature and the amount of maintenance required in the long run.

---

1. 我们在下面的 To-do list 中罗列了一些应用场景和待实现的功能，欢迎大家选择其中任何一项功能做实现。

* 修改进程通信模块
* 建立行人，车辆，猫狗等常见检测模型
* 禁入区等功能（免训练）
* 中文语音识别
* 身份证，发票等常见OCR功能（免训练）
* 手势识别，人体姿态特征点检测，人脸特征点检测（免训练）
* 图像分割，要有相应的常见模型
* 通用 OCR
* 视频追踪 (Work-In-Progress)

2. 如果您想提供 To-do list 中没有的功能，我们也十分欢迎。请在提交时告诉我们这项功能的重要性，并举例相关落地场景。我们会权衡新功能的实用性及维护成本，决定是否接受您的贡献。

## Pull Request Process

1. Please ensure that each pull request only contains the implementation or modification for ONE feature, without any modification that is irrelevant to the dedicated feature. If you would like to implement more than one feature (it will be well-appreciated!), please start a pull request for each distinct feature.

2. In your pull request for adding new features, please include the following information in order to help others review your code:

* A README to explain the purpose of such feature
* Interfaces
* Any new global/local variables that may affect other parts of the project
* File directories
* Any libraries used
* Configurations

3. Please ensure that all dependency issues are cleared before submitting the PR

4. Please follow [PEP8](https://www.python.org/dev/peps/pep-0008/)  style guide.

---

1. 请确保每个 pull request 都只是一个特定功能或者改进。请不要包含其他不相关的改进。如果您想实现或修改多个功能，请为每个功能或改进建立多个独立的 pull request。

2. 在您的每个新功能的 PR 中请务必写好相应的：
* README 来阐述功能
* 接口
* 新引入的，有可能对外部有影响的，全局/环境变量等
* 文件路径
* 用到的库
* 配置项

3. 请在提交代码前处理好所有的依赖项。

4. 请使用 [PEP8](https://www.python.org/dev/peps/pep-0008/) 编码规范。

 
