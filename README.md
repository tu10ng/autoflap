autoflap
==
根据8111端口的 flaps 的值不断按下 `f` 和 `r` (放下或收起襟翼) 将襟翼值控制在一个固定值

如果需要改变 flaps 的值, 打开 .config.csv 修改. 

目前只支持 Windows

欢迎 issues 和 pull requests

## Usage
### requirements
需要在 wt 里单独设置 `f` 和 `r` 键, 分别对应 开启襟翼 和 关襟翼

### 运行
运行 release 里的 .exe 文件

### behaviour
如果不是飞机(8111端口没有返回 flaps 值); 或在车库看飞机里, 而不是在战斗中; 或前台窗口不是战雷时, 不输出按键.

如果是飞机, 且在战斗中, 且前台窗口是战雷, 才输出按键.

- 在输出按键时, 如果按 `win` 键(为了切换前台程序), 有可能会输出 `win + r` 或 `win + f`

#### 暂停
按下键盘上的 `Pause` 键会让程序暂停/继续

- 进入睡眠状态时, 会按下三次r, 这意味着:
  - 如果想睡眠并设定襟翼值为第二档: 
    按下 `Pause` 后连续按下两次 `f` 

请不要按着 Pause 不松手. 如果有bug, 可以试一试按下时多按零点几秒有没有帮助(并告诉我)

暂停这里由于库的原因, 一直有判断问题:
- 比如在按下 `Pause` 后的零点几或零点零几秒左右时间内, 程序不会对下次 `Pause` 作出响应
- 或者运行时按pause不暂停
如果遇到, 请记录发生bug时的情况并告诉我.


#### 退出
- 直接关闭 .exe 运行后弹出的黑色终端, 

### 修改配置
程序会在 .config.csv 修改后自动读取, 无需重启或暂停程序.

各选项说明:
- target_value: 希望飞机襟翼处于的稳定值 (襟翼张开百分比)
  比如 8 代表稳定于 8% 的襟翼

## build/test
### dependencies
打开 terminal, 或者 powershell 或 cmd (以下称终端),

run:

    pip install -r requirements.txt

### run
在终端中运行:

    python ./autoflap.py
    
### 退出
- 按 `Ctrl-c`

## known problems
- under `working', very very fast concequtive of pause would stuck after going to sleep
  after testing, its because of the 3 presses of r
- the keyboard module will make program slower when pressing f/r, maybe because it will block main thread execution, or its because the underlying sending mechanism will block execution
  
## TODO
- make 'print messages' more readable, like "in flight * 3"
- 把要处于的稳定襟翼值显示在屏幕上
- 语音提示有没有捕捉到Pause
- 为不同机型提供预设值
