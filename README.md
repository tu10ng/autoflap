autoflap
==
根据8111端口的 flaps 的值不断按下 `f` 和 `r` (放下或收起襟翼) 将襟翼值控制在一个值

目前只支持 Windows

欢迎 issues 和 pull requests

## Usage
### requirements
需要在 wt 里单独设置 `f` 和 `r` 键, 分别对应 开启襟翼 和 关襟翼

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

- 如果在运行状态, 按下 `Pause` 后, 会按下三次r, 将襟翼收起至0, 然后暂停(不等待松开)
  - 此时如果想设定襟翼值, 比如设定为第二档, 只需如下操作: 按下 `Pause` 后连续按下两次 `f` 即可
- 如果在睡眠状态, 在 `Pause` 按下并且松开后, 才会继续(和上面的行为不同)

#### 退出
- 直接关闭 .exe 运行后弹出的黑色终端, 
- 在运行python的终端里, 按 `Ctrl-c`

### 修改配置
如果需要改变 flaps 的值, 打开 .config.csv 修改. 

程序在运行期间会检测 config 文件是否修改并重新读取.

各选项说明:
- threshold: 稳定值
- time_interval: 每次循环的间隔时间
- thres_range_sup/inf: 检测区间为 [ threshold - thres_range_inf, threshold + thres_range_sup ]

## build/test
### dependencies
打开一个 powershell 或 cmd (以下称终端),

run:

    pip install -r requirements.txt

### run
在终端中运行:

    python ./autoflap.py

## known problems
- python module `curses` dont behave well on Windows.
- python module `ahk` block thread.

## TODO
- 把要处于的稳定襟翼值显示在屏幕上
- 测试 thres_range 和 time_interval 不同值对不同襟翼开关速度飞机的影响
- 语音提示开启与否
- 为不同机型提供预设值
