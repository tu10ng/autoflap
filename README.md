autoflap
==
根据8111端口的 flaps 的值不断按下f和r来放下或收起襟翼
目前只支持 Windows

欢迎 issues 和 pull requests

## Usage
### requirements
需要在 wt 里单独设置 f 和 r 键

还需要打开一个 powershell 或 cmd (以下称终端),

run:

    pip install -r requirements.txt
    
### behaviour
#### 运行
运行 .exe 文件, 或者在终端中运行:

    python ./autoflap.py
    
如果不是飞机, 或者战雷没运行, 就持续睡眠, 直到上飞机为止.

期间每五秒检测一次, 应该没有感觉.

目前因为无法自动检测前台程序, 运行后默认暂停状态.

#### 暂停
按下键盘上的 `Pause` 键会让程序暂停/继续

#### 修改配置
如果需要改变 flaps 的值, 打开 .config.csv 修改. 

程序在运行期间也会检测 config 文件的修改并重新读取.

#### 退出
- 直接关闭 .exe 运行后弹出的黑色终端, 
- 在运行python的终端里, 按 `Ctrl-c`

## known problems

## TODO
- web based configuration interface (like fish shell)
- detect focus windows' name
