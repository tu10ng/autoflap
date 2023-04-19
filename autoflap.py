import re
import requests
import keyboard
import time
import os
import csv
import ctypes

# the value user wants. should be customizable outside of src.
threshold = 15
# the threshold can change +-1
thres_range_sup = 1
thres_range_inf = 1
thres_max = threshold + thres_range_sup
thres_min = threshold - thres_range_inf

time_interval = 0.1

config_file = "./.config.csv"
config_file_mtime = 0


def recalc_thres_range():
    # its bit tedious to use class to just hold things we could type in two words
    globals()["thres_max"] = threshold + thres_range_sup
    globals()["thres_min"] = threshold - thres_range_inf


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

    recalc_thres_range()


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


def control_flaps(flaps):
    # the additional else is to avoid oscillation
    if flaps >= thres_max:  # press r
        # must release f/r, the release in else sometime is missed
        keyboard.release("f")
        # cant use `press_and_release' due to unkown error
        keyboard.press("r")
    elif flaps <= thres_min:  # press f
        keyboard.release("r")
        keyboard.press("f")
    else:
        keyboard.release("r")
        keyboard.release("f")


if __name__ == "__main__":
    session = requests.Session()
    while True:
        time.sleep(time_interval)

        # `Pause' to sleep the program
        if keyboard.is_pressed("pause"):
            print("sleeping")
            time.sleep(0.5)
            keyboard.wait("pause")
            time.sleep(0.3)  # if too small, will trigger pause in next loop

        # ensure read config_file on startup
        try:
            if os.path.getmtime(config_file) > config_file_mtime:
                update_config()
        except Exception as e:
            print("Error: no configuration file detected, default to 15.")

        # if not in plane, we will loop in here
        flaps = get_flaps()
        while flaps == None:
            print("还没上天")
            time.sleep(5)
            flaps = get_flaps()

        print("上天!: ", flaps)

        # if in plane, dont press keys when focus windows isnt wt
        if in_wt():
            control_flaps(flaps)
