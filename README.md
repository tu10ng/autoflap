autoflap
==
根据8111端口的 flaps 的值不断按下f和r来放下或收起襟翼
目前只支持 Windows

欢迎 issues 和 pull requests

## Usage
### requirements
需要在 wt 里单独设置 f 和 r 键, 还要打开一个 powershell 或 cmd (以下称终端),

run:

    pip install -r requirements.txt
    
### behaviour
在终端中运行:

    python ./autoflap.py
    
默认运行后是停止状态, 按下键盘上的 `Pause` 键会让程序运行, 再次按下 `Pause` 会让程序再次停止.

完全终止程序, 请在运行上面命令的终端里按 `Ctrl-c`

## TODO
- detect wt(aecs) and auto enable/disable
- detect whether in plane or not

