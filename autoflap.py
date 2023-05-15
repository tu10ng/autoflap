import re
import requests
import keyboard
import time
import os
import csv
import ctypes

# the value user wants. should be customizable outside of src.
target_value = 15

config_file = "./.config.csv"
config_file_mtime = 0


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


def get_flaps():
    """return value of flaps.
    return None if not in plane or wt not running"""
    try:
        state = session.get("http://127.0.0.1:8111/state").json()
    except Exception as e:
        print("\rwar thunder isn't running: ", e, end="")
        return None

    if state["valid"] == False:
        return None

    flaps = state["flaps, %"]
    return flaps


def update_config():
    """the update method we take means config file must have the same name
    with global variables."""
    with open(config_file) as f:
        reader = csv.reader(f, delimiter=" ")
        for k, v in reader:
            globals()[k] = float(v)  # globals()['threshold']


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
    # print(front_window)
    if re.search("War Thunder - ", front_window):
        # print("in battle")
        return True
    else:
        # print("not in battle")
        return False


class Press(object):
    """
    we must `press', and wait for a `time_interval', then `release',
    to make wt recognize our key input.
    and we cant use `press_and_release'
    """

    time_interval = 0.005

    def __init__(self, key):
        self.key = key

    def __enter__(self):
        keyboard.press(self.key)

    def __exit__(self, *args):
        # 0.003 is min but unstable, flap go beyond
        # 0.005 is very good after test
        time.sleep(self.time_interval)
        self.release_fr()

    def release_fr(self):
        keyboard.release("f")
        keyboard.release("r")


def control_flaps(flaps):
    # TODO: is equal effect flaps stability
    if flaps >= target_value:
        with Press("r"):
            pass
    else:
        with Press("f"):
            pass


def wait_release(key):
    while keyboard.is_pressed(key):
        pass


if __name__ == "__main__":
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
    session = requests.Session()
    while True:
        # `Pause' to sleep the program
        if keyboard.is_pressed("pause"):
            wait_release("pause")
            if in_wt():
                with Press("r"):  # release flap immediately before release `pause'
                    pass
                with Press("r"):
                    pass
                with Press("r"):
                    pass

            print("sleeping")

            while True:
                time.sleep(0.01)
                if keyboard.is_pressed("pause"):
                    wait_release("pause")
                    print("awoke, ", end="")
                    break

            print("working")

        # ensure read config_file on startup
        try:
            if os.path.getmtime(config_file) > config_file_mtime:
                update_config()
                config_file_mtime = os.path.getmtime(config_file)
        except Exception as e:
            print("Error: no configuration file detected, default to 15: ", e)

        # if not in plane, we will loop in here
        # TODO: not in battle shouldnt go outside loop
        flaps = get_flaps()
        while flaps == None:
            print("还没上天")
            time.sleep(5)
            flaps = get_flaps()

        print("上天!: ", flaps)

        # if in plane, dont press keys when focus windows isnt wt
        if in_wt():
            control_flaps(flaps)
