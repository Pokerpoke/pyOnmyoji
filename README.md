# pyOnmyoji脚本

阴阳师护肝脚本。

提供一些API供mod开发。

## 安装依赖

- 安装[python3.7](https://www.python.org/ftp/python/3.7.7/python-3.7.7.exe)，python3.8未测试

- 双击`install.bat`，等待依赖安装完成

## 运行方式

- 右击`start.bat`->管理员权限运行

## 运行相对稳定功能

- 困28
- 觉醒
- 御魂
- 御魂（队员）

## 所有mod

- 花合战：
  - 需要有一套能刷困二十八的阵容，一套御魂的阵容，一套觉醒的阵容，并保证不会翻车
  - 将会执行百鬼夜行1次，御魂17次，觉醒13次，困二十八7次
- 困28，设定次数后，点击开始
  - 可启动界面：庭院、探索、困28（有探索按钮的那个框）、进入困28的战斗界面进入
  - 默认开启金币、经验加成
  - 自动换狗粮，狗粮队长放到最左侧位置，其余两个位置放置狗粮，目前仅支持更换白蛋
- 百鬼夜行：设定次数后，点击开始
  - 可启动界面：庭院、百鬼夜行
  - 随机邀请好友
- 御魂：设定次数后，点击开始
  - 自动开启加成
  - 可启动界面：庭院、探索、御魂
- 觉醒：设定次数后，点击开始
  - 自动开启加成
  - 可启动界面：庭院
- 御灵：设定次数后，点击开始
  - 可启动界面：庭院、探索、御灵
- 协作任务（未完成）：自动接受、拒绝协作任务
- 御魂（队员）：
  - 自动开启加成
  - 在庭院中点击开始，会自动接受邀请并进行战斗
  - 注意：每次等待最长时间为5分钟
  - 会自动进行点赞
- 御魂（队长）：
- 御灵：
- 加成：开启加成，主要供其他mod调用
- 友情点：
  - 赠送友情点，领取并回赠友情点

## mod开发

- 识别测试(match_test)：自动截图并对`mods/match_test/img/template.png`进行匹配测试
- 模块测试(mod_test)：测试相关功能

TODO:

## TODO:

[TODOS](https://github.com/Pokerpoke/pyOnmyoji/projects/1)
