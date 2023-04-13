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
在终端中运行:

    python ./autoflap.py
    
默认运行后如果不是飞机, 或者战雷没运行, 就持续睡眠, 直到上飞机为止.

期间每五秒检测一次, 应该没有感觉.

(bug): 目前不仅飞机战斗中, 在车库里看飞机时也会输出按键, 因此需要一个的暂停/继续键:

按下键盘上的 `Pause` 键会让程序暂时暂停, 再次按下 `Pause` 会让程序继续运行. 

完全终止程序, 请在运行上面命令的终端里按 `Ctrl-c`

## TODO
- config file
- web based configuration interface (like fish shell)
