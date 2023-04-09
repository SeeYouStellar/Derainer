## My Graduate design:Derainer based on Raspberry Pi

## file structure
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
│      Gui.py
│      ShowVideo.py
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
│      ShowVideo.py
└─__pycache__

```
