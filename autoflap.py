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
    except Exception as _:
        return None

    if state["valid"] == False:
        return None

    # we use this to detect in garage instead of in battle
    # we cant get battle state from 8111/state, only from 8111
    if state["thrust 1, kgs"] == 0:
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
    return re.search("War Thunder - ", front_window)


def press(key: str):
    """
    we must `press', and wait for a `time_interval', then `release',
    to make wt recognize our key input.
    and we cant use `press_and_release'

    0.003 is min but unstable, flap go beyond
    0.005 is very good after test
    0.01 is also good
    """
    time_interval = 0.005

    keyboard.press(key)

    time.sleep(time_interval)
    keyboard.release("f")
    keyboard.release("r")


def control_flaps(flaps):
    # TODO: is equal effect flaps stability
    if flaps >= target_value:
        press("r")
    else:
        press("f")


def wait_release(key):
    while keyboard.is_pressed(key):
        pass


def print_cat_sleep():
    print("\033[H\033[2J\033[0m")
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
    print("\033[0;36msleeping\033[0m")


def print_cat_awake():
    print("\033[H\033[2J\033[0m")
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
    print("\033[0;32mawake\033[0m")


if __name__ == "__main__":
    os.system("")  # for ansi control sequence to work
    print_cat_awake()
    session = requests.Session()

    while True:
        # `Pause' to sleep the program
        if keyboard.is_pressed("pause"):
            wait_release("pause")
            press("r")
            time.sleep(0.005)
            press("r")
            time.sleep(0.005)
            press("r")

            print_cat_sleep()

            while True:
                time.sleep(0.01)
                if keyboard.is_pressed("pause"):
                    wait_release("pause")
                    break

            print_cat_awake()

        # ensure read config_file on startup
        try:
            if os.path.getmtime(config_file) > config_file_mtime:
                update_config()
                print(f"\033[0;32mnew configuration: {target_value}\033[0m")
                config_file_mtime = os.path.getmtime(config_file)
        except Exception as e:
            print(f"\033[0;31mError: cant read configuration: {e}\033[0m")

        # if not in battle, we will loop in here
        flaps = get_flaps()
        while flaps == None:
            print("\r\033[0;36m还没上天     \033[0m", end="")
            time.sleep(5)
            flaps = get_flaps()

        print(f"\r\033[0;33m上天!: {flaps}     \033[0m", end="")

        # dont press keys when focus windows isnt wt
        if in_wt():
            control_flaps(flaps)
