import re
import requests
import keyboard
import time
import os
import csv

# the value user wants. should be customizable outside of src.
threshold = 15
# the threshold can change +-1
thres_range = 1
thres_max = threshold + thres_range
thres_min = threshold - thres_range

config_file = "./.config.csv"
config_file_mtime = 0


def recalc_thres_range():
    # its bit tedious to use class to just hold things we could type in two words
    globals()['thres_max'] = threshold + thres_range
    globals()['thres_min'] = threshold - thres_range

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
        state = session.get('http://127.0.0.1:8111/state').json()
    except Exception as e:
        return None
    
    if state['valid'] == False:
        return None
    
    flaps = state['flaps, %']
    return flaps


def update_config():
    """ the update method we take means config file must have the same name
    with global variables. """
    with open(config_file) as f:
        reader = csv.reader(f, delimiter=' ')
        for k, v in reader:
            globals()[k] = int(v)    # globals()['threshold']

    recalc_thres_range()


if __name__ == '__main__':
    session = requests.Session()
    keyboard.wait("pause")
    time.sleep(0.2)
    while True:
        time.sleep(0.1)
        if keyboard.is_pressed("pause"):
            time.sleep(0.2)
            keyboard.wait("pause")
            time.sleep(0.2)

        flaps = get_flaps()
        while flaps == None:
            print("还没上天")
            time.sleep(5)
            flaps = get_flaps()

        # ensure read config_file on startup
        try:
            if os.path.getmtime(config_file) > config_file_mtime:
                update_config()
        except Exception as e:
            print("Error: no configuration file detected, default to 15.")
                             
        print("上天!: ", flaps)
        # with release in additional else, maybe we can avoid oscillation
        if flaps >= thres_max:
            # press r
            keyboard.release("f")            
            keyboard.press("r")
            continue
        elif flaps <= thres_min:
            # press f
            keyboard.release("r")
            keyboard.press("f")
            continue
        else:
            keyboard.release("r")
            keyboard.release("f")
            continue
