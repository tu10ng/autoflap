autoflap
==
将襟翼控制在设定值附近, 相当于增加一个额外的襟翼档位, 比如给你的喷火加上一个作战档.

如果需要改变设定值, 打开 .config.csv 修改. 

目前只支持 Windows

欢迎 issues 和 pull requests

## [傻瓜式教程](./傻瓜式教程.txt)

## 修改源代码
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
