import json
import re
import requests
import keyboard
import time
import os
import ctypes
import multiprocessing as mp
import queue
from dataclasses import dataclass

# state的返回值如下
# {"valid"                   : true,
# "aileron, %"               : -0,
# "elevator, %"              : 19,
# "rudder, %"                : 1,
# "flaps, %"                 : 13,
# "gear, %"                  : 0,
# "H, m"                     : 598,
# "TAS, km/h"                : 223,
# "IAS, km/h"                : 217,
# "M"                        : 0.18,
# "AoA, deg"                 : 3.2,
# "AoS, deg"                 : 0.2,
# "Ny"                       : 0.94,
# "Vy, m/s"                  : 19.4,
# "Wx, deg/s"                : 0,
# "Mfuel, kg"                : 123,
# "Mfuel0, kg"               : 410,
# "throttle 1, %"            : 97,
# "RPM throttle 1, %"        : 100,
# "radiator 1, %"            : 0,
# "magneto 1"                : 3,
# "power 1, hp"              : 1465.0,
# "RPM 1"                    : 2387,
# "manifold pressure 1, atm" : 1.30,
# "oil temp 1, C"            : 73,
# "pitch 1, deg"             : 31.0,
# "thrust 1, kgs"            : 1304,
# "efficiency 1, %"          : 73}

# return {'valid': False} if not in plane


def send_flaps(mkq: mp.Queue, awoke):
    session = requests.Session()

    def read_8111():
        """
        return value of flaps.
        return None if not in plane or wt not running
        """
        try:
            state = session.get("http://127.0.0.1:8111/state").json()
        except Exception as e:
            print(e)
            return None

        if state["valid"] == False:
            return None

        return state["flaps, %"]

    while True:
        awoke.wait()
        # if not in plane, we will loop in here
        # time sleep here must not be too small, or mkq will not be empty
        time.sleep(0.002)
        flaps = read_8111()
        if flaps == None:
            print("还没上天")
            time.sleep(5)
        else:
            # print("send ", flaps)
            mkq.put(("flaps", flaps))


def control_flaps(mkq: mp.Queue, awoke):
    """
    mkq is a message queue
    """
    flaps: int = 0
    target_value: int = 15
    time_interval: float = 0.001

    while True:
        awoke.wait()
        if time_interval > 0:
            time.sleep(time_interval)

        try:
            # only update data when new data arrives
            # get two times to (try to) make mkq empty
            for _ in range(2):
                if msg := mkq.get_nowait():
                    if msg[0] == "flaps":
                        flaps = msg[1]
                    elif msg[0] == "config":
                        data = msg[1]
                        target_value = data["target_value"]
                        time_interval = data["time_interval"]
        except queue.Empty:
            pass

        # print(mkq.empty())
        # no flash on Windows
        print(f"\033[5;33m上天!: {flaps}   \033[0m", end="\r")

        if in_wt():
            if flaps >= target_value:
                press_key("r")
            else:
                press_key("f")


@dataclass
class Config:
    path: str = "./config.json"
    mtime: float = 0.0


def send_config(mkq: mp.Queue, awoke):
    def make_msg(config: Config):
        """
        return None if config file isnt modified.
        else returns a tuple like ('config', JSON_DATA), example:
        ('config', {'target_value': 15, 'time_interval': 0.01})

        """
        # TODO global value
        try:
            if os.path.getmtime(config.path) > config.mtime:
                config.mtime = os.path.getmtime(config.path)
                with open(config.path) as f:
                    data = json.load(f)
                    print(f"\033[0;32mnew configuration: {data}\033[0m")
                    return ("config", data)
        except Exception as e:
            # TODO: 15 isn't global
            print(f"\033[0;31mError: loading configuration file: {e}.\033[0m")

        return None

    # send_config
    config = Config()
    while True:
        awoke.wait()

        time.sleep(1)
        msg = make_msg(config)
        if msg != None:
            mkq.put(msg)


# ret value:
# 'st.py - st - Visual Studio Code'
# 'War Thunder - Test Flight'
# 'War Thunder'
def getWindow():
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
    # buff.value is the title of the window, hwnd is the window handle
    return buff.value


def in_wt():
    """
    "War Thunder" means in garage, which we will skip
    "War Thunder - Test Flight" in test flight, which we want

    ground battle would not fall into this function(will sleep in outter function)

    TODO: other circumstances aren't yet tested
    """
    front_window = getWindow()
    return True if re.search("War Thunder - ", front_window) else False


def press_key(key: str):
    """
    important: have a delay of 0.?s.
    """
    interval = 0.0001
    keyboard.press(key)
    time.sleep(interval / 2)
    keyboard.release("f")
    keyboard.release("r")
    time.sleep(interval / 2)


def print_cat():
    print(
        r"""
 
           |\___/|
           )     (             .              '
          =\     /=
            )===(       *
           /     \
           |     |
          /       \
          \       /
   _/\_/\_/\__  _/_/\_/\_/\_/\_/\_/\_/\_/\_/\_
   |  |  |  |( (  |  |  |  |  |  |  |  |  |  |
   |  |  |  | ) ) |  |  |  |  |  |  |  |  |  |
   |  |  |  |(_(  |  |  |  |  |  |  |  |  |  |
   |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
   |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

"""
    )


def print_cat2():
    print(
        r"""
                  .
           __..--''``\--....___   _..,_
       _.-'    .-/";  `        ``<._  ``-+'~=.
   _.-' _..--.'_    \                    `(^) )
  ((..-'    (< _     ;_..__               ; `'
             `-._,_)'      ``--...____..-'
                                      fxlee

"""
    )


if __name__ == "__main__":
    mp.set_start_method("spawn")  # default on windows, but not linux
    os.system("")  # for ascii control sequence
    k = ctypes.windll.kernel32
    k.SetConsoleMode(k.GetStdHandle(-11), 7)
    mkq = mp.Queue()
    awoke = mp.Event()  # if set->run; clear->sleep
    awoke.set()

    print_cat()
    p0 = mp.Process(target=send_flaps, args=(mkq, awoke))
    p1 = mp.Process(target=control_flaps, args=(mkq, awoke))
    p2 = mp.Process(target=send_config, args=(mkq, awoke))
    p0.start()
    p1.start()
    p2.start()

    while True:
        # `Pause' to sleep the program
        keyboard.wait("pause", True, True)
        awoke.clear()

        # reset flap
        if in_wt():
            press_key("r")
            press_key("r")
            press_key("r")

        # clear screen
        print("\033[H\033[2Jsleeping\033[0m")
        print_cat2()

        keyboard.wait("pause", True, True)
        awoke.set()
        print("\033[H\033[2Jawoke\033[0m")
        print_cat()
