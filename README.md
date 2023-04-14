autoflap
==
根据8111端口的 flaps 的值不断按下 `f` 和 `r` (放下或收起襟翼) 将襟翼值控制在一个值

目前只支持 Windows

欢迎 issues 和 pull requests

## Usage
### requirements
需要在 wt 里单独设置 `f` 和 `r` 键

### 运行
运行 release 里的 .exe 文件

### behaviour
如果不是飞机(8111端口没有返回 flaps 值), 就持续睡眠.

每五秒检测一次(应该没有感觉).

如果是飞机, 如果前台窗口不是战雷, 不输出按键.

如果是飞机, 但是在车库里, 而不是在战斗中, 不输出按键.

如果是飞机, 且在战斗中, 才输出按键.

#### 暂停
按下键盘上的 `Pause` 键会让程序暂停/继续

#### 修改配置
如果需要改变 flaps 的值, 打开 .config.csv 修改. 

程序在运行期间也会检测 config 文件的修改并重新读取.

#### 退出
- 直接关闭 .exe 运行后弹出的黑色终端, 
- 在运行python的终端里, 按 `Ctrl-c`

## build/test
### dependencies
打开一个 powershell 或 cmd (以下称终端),

run:

    pip install -r requirements.txt

### run
在终端中运行:

    python ./autoflap.py

## known problems
- if press f/r for a long time, the `control_flaps` function stop to correct send f/r. repress f/r to let flaps fall back to threshold cant solve this problem

## TODO
- make 'print messages' more readable, like "in flight * 3"
