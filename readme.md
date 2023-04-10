## My Graduate design:Derainer based on Raspberry Pi

### file structure
```shell
│  readme.md
├─.idea
│  │  .gitignore
│  │  CVPR17_training_code.iml
│  │  misc.xml
│  │  modules.xml
│  │  vcs.xml
│  │  workspace.xml
│  └─inspectionProfiles
│          profiles_settings.xml
│          Project_Default.xml
├─Client
│      main.py
│      ListenVideo.py
├─Network
│  │  GuidedFilter.py
│  │  testing.py
│  │  training.py
│  ├─model
│  │  └─trained
│  │          model.data-00000-of-00001
│  │          model.index
│  ├─TestData
│  │  ├─input
│  │  │      1.jpg
│  │  │      2.jpg
│  │  └─results
│  │          1.png
│  │          2.png
│  └─TrainData
│      ├─input
│      │      1.jpg
│      │      2.jpg
│      └─label
│              1.jpg
│              2.jpg
├─Server
│      ListenVideo.py
└─__pycache__

```

### Gui design

1. 打开系统，系统就开始监听树莓派传输过来的摄像头镜头画面

2. 点击显示镜头，命令树莓派开始传输镜头画面，镜头出现在系统界面中

3. 点击开始拍照，将点击时的一帧截取并保存至本地，并命令树莓派关闭视频传输，将该帧定格到系统界面中

4. 点击去雨处理，将该帧传输给树莓派，命令树莓派运行去雨代码，并将结果图像返回给系统

5. 点击结果评估，调用评估代码评估本地的原图和结果图， 返回值显示到系统界面