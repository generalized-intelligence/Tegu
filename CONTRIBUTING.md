# Roadmap

Tegu is a rapid development toolkit, designed for non-ML programmers to develop machine learning enabled solutions. Therefore, the GUI component of the toolkit is crucial. We would like to simplify the training process to the greatest extent. In some case, we even provide training-free solutions for machine learning tasks. With HTTP protocols, users do not need to use any machine learning related programming. Any languages that are compatible with HTTP protocols can be used to communicate with Tegu.

The project is consist of two parts: Network and GUI.

Network: this part currently has implementations in image recognition, video classification, facial recognition, and license plate recognition.

GUI: this part contains the GUI for existing networks and HTTP API.

We would like to cover as many use cases as possible, so one of the major goals is to add a variety of neural networks to fulfill demands in different use cases.

---

## Contribute to Tegu

Welcome to Tegu and we would like to thank you for your contribution in advance! If you have decided to contribute to Tegu, you may join [![Join the chat at https://gitter.im/Tegutalk/community](https://badges.gitter.im/Tegutalk/community.svg)](https://gitter.im/Tegutalk/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) to participate in the discussion. If someone else is interested in what you are working on, we will direct him/her to you.

---

首先，感谢你能够想到为 Tegu 做出贡献! 如果你真的决定为 Tegu 做出贡献，你可以加入 [![Join the chat at https://gitter.im/Tegutalk/community](https://badges.gitter.im/Tegutalk/community.svg)](https://gitter.im/Tegutalk/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) 与我们一起讨论。我们会尽可能地帮助你解决问题。如果有其他人与你的目标重合，我们帮助你找到有同样目标的人。

### New Features

There are two major components in Tegu, GUI and Tegu-core.

Tegu-core can be found in the `\Network` folder, including realizations for different use cases. Tegu-core also contains codes for HTTP API and external communication.

The GUI component is critical to Tegu, because one of the main goals of Tegu is to minimize the amount of coding required in machine learning development. The GUI component can be found in the `\GUI` folder. It includes the user interfaces for different features (such as training and prediction for image detection) or different realizations of the same feature, as well as the demonstration of outcomes delivered by the feature (for example, real-time training loss).

If you would like to help us realize new features:

1. We welcome and appreciate all contributions toward any one of the topics in the following to-do-list:

* Optimization of interprocess communication
* Adding common neural networks, such as passenger detection, vehicle detection, and cat/dog detection
* Abnormality Detection in Restricted Zone (Training Free)
* Chinese NLP
* OCR for common documents, such as personal identifications or receipts (Training Free)
* Hand Gesture Recognition, Pose Detection based on Feature Point Paring, Facial Feature Point Detection (Training Free)
* Image Segmentation
* General OCR
* Video Tracking (Work-In-Progress)

2. If you would like to build the GUI component for a feature that you added, or for a new realization for an existing feature, please start a separate PR from the core-code of the feature.

3. Please try to use the same version of libraries and infrastructures as the ones already being used. If you would like to introduce new libraries and infrastructures, please clearly list the libraries and required version.

4. We are more than grateful if you are kind enough to make the GUI components for features that do not have GUI yet.  Your contributions are valuable for non-programmers in Tegu community.

5. We are working on building our own style guide. In the meanwhile, please follow [PEP8](https://www.python.org/dev/peps/pep-0008/).

6. In your pull request for adding new features, please include the following information in order to help others review your code:

* A README to explain the purpose of such feature
* Interfaces
* Any new global/local variables that may affect other parts of the project
* File directories
* Any libraries used
* Configurations

7. Please ensure that all dependency issues are cleared before submitting the PR

Feel free to ask any questions at [![Join the chat at https://gitter.im/Tegutalk/community](https://badges.gitter.im/Tegutalk/community.svg)](https://gitter.im/Tegutalk/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge), someone will be able to point you to the right direction.

---

Tegu 大致分成两个部分， GUI 和 Tegu-core 部分。Tegu-core 部分主要集中在 `\Network` 文件夹下，包含不同功能的实现，或者相同功能的不同实现。 Tegu-core 部分包含 HTTP API 与外界通信。

Tegu 的一大目标就是让用户尽可能少的接触代码，所以我们还需要 GUI 部分来让 Tegu 变得更加易用。 GUI 部分集中在 `\GUI` 文件夹下，包括对每个功能的图形化界面的操作（如图像检测的训练和预测），也包含对使用期间输出信息的展示（如训练时显示实时的 loss 等）。

如果你想帮助我们实现新的功能:

1. 我们在下面的 To-do list 中罗列了一些应用场景和待实现的功能，欢迎大家选择其中任何一项功能做实现：

* 修改进程通信模块
* 建立行人，车辆，猫狗等常见检测模型
* 禁入区等功能（免训练）
* 中文语音识别
* 身份证，发票等常见OCR功能（免训练）
* 手势识别，人体姿态特征点检测，人脸特征点检测（免训练）
* 图像分割，要有相应的常见模型
* 通用 OCR
* 视频追踪 (Work-In-Progress)

2. 如果在实现了一个新的应用场景，或者添加了一个已有应用场景的新实现后，你还想完成该功能的 GUI 部分，请为 GUI 模块单独新建一个 pull request。
3. 请尽量使用已有的框架或包的当前已经在使用的版本，如果你需要添加新的包或者框架，请注明所用到的包和版本。
4. 如果你发现有些功能还没有相对应的 GUI ，我们非常欢迎你完成相应的 GUI ，并感激你为社区中非程序员用户使用 Tegu 做出的贡献。
5. 我们正在编写属于我们的命名规范，于此同时，请尽量使用 [PEP8](https://www.python.org/dev/peps/pep-0008/) 编码规范。
6. 在您的每个新功能的 PR 中请务必写好相应的：
* README 来阐述功能
* 接口
* 新引入的，有可能对外部有影响的，全局/环境变量等
* 文件路径
* 用到的库
* 配置项
7. 请确保在提交代码之前已经处理好所有的依赖项。

如果你在实现功能时遇到了问题，可以联系我们 [![Join the chat at https://gitter.im/Tegutalk/community](https://badges.gitter.im/Tegutalk/community.svg)](https://gitter.im/Tegutalk/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) ，我们会尽力帮助你。

### Issues

Submitting issues is also a great way to contribute to the community. Below are some tricks to help us understand what has happened:

* Tell us what you expected to happen
* Tell us what happened in reality. If this is an Exception, please paste the entire Trackback.
* If possible, paste your code to help us locate and resolve the issue.
* List the operating environment (Windows or Linux, version of Keras and Tensorflow)

See the [Guideline to Create Minimal, Complete, and Verifiable Issue](https://stackoverflow.com/help/mcve) for an example.

---

我们欢迎你向 Tegu 提交 issue ，这能够帮助我们有效的改进 Tegu。以下是一些提交 issue 时的建议，可以帮助我们更好的了解和定位这个 issue:

* 请描述你期待发生什么事情。
* 请描述实际发生了什么事情，如果是一个 Exception 请粘贴完整的 Trackback。
* 如果有可能，贴上一些代码，能够帮助我们定位和解决问题。
* 贴出你的运行环境。(Windows or Linux，Keras 和 Tensorflow 的版本)

可以参考[最小，完整，可验证](https://stackoverflow.com/help/mcve)的标准提出 issue 。

### Testing

It would be great if testing is done before submitting the PR. If possible, please include the test case.

---

在提交之前最好完成测试，如果可以的话给出测试用例是再好不过的了。

### Help with Compiling

As new libraries and infrastructures may be needed for new features, we may need to change how we release the software in the future. One of the main goals of Tegu is to minimize the amount of coding required for machine learning development. Therefore, providing executable GUI-based software is critical.

Currently, Tegu supports Windows 10. If you have found out the existing executable software is not in sync with the code-only software, feel free to provide:

* Executable file. You may contact us at [![Join the chat at https://gitter.im/Tegutalk/community](https://badges.gitter.im/Tegutalk/community.svg)](https://gitter.im/Tegutalk/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) to upload your packed and compressed executable file and testing environment.
*  Packed scripts and user manuals of any form.

---

由于新的应用场景很可能需要新的框架或者包，我们可能需要不断更新 Release 方式，由于 Tegu 的一大目标是让用户少接触代码，所以能够生成一个纯 GUI 的可执行程序是非常必要的。

目前 Tegu 支持 Windows 10 环境，如果你发现目前提供的可执行程序的版本比纯代码版本落后，我们欢迎并感谢你提供：

* 打包后的可执行程序文件。你可以联系我们 [![Join the chat at https://gitter.im/Tegutalk/community](https://badges.gitter.im/Tegutalk/community.svg)](https://gitter.im/Tegutalk/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) 上传你打包过后的压缩文件，并请提供你测试的系统环境。
* 打包的脚本，和任何形式的说明文档。
