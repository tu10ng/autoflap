import re
import requests
import keyboard
import time

# state的返回值如下
# state = """{"valid": true,
# "aileron, %": -0,
# "elevator, %": 19,
# "rudder, %": 1,
# "flaps, %": 13,
# "gear, %": 0,
# "H, m": 598,
# "TAS, km/h": 223,
# "IAS, km/h": 217,
# "M": 0.18,
# "AoA, deg": 3.2,
# "AoS, deg": 0.2,
# "Ny": 0.94,
# "Vy, m/s": 19.4,
# "Wx, deg/s": 0,
# "Mfuel, kg": 123,
# "Mfuel0, kg": 410,
# "throttle 1, %": 97,
# "RPM throttle 1, %": 100,
# "radiator 1, %": 0,
# "magneto 1": 3,
# "power 1, hp": 1465.0,
# "RPM 1": 2387,
# "manifold pressure 1, atm": 1.30,
# "oil temp 1, C": 73,
# "pitch 1, deg": 31.0,
# "thrust 1, kgs": 1304,
# "efficiency 1, %": 73}"""
if __name__ == '__main__':
    session = requests.Session()
    # for i in range(3):
    keyboard.wait("pause")
    time.sleep(0.2)
    while True:
        time.sleep(0.1)
        if keyboard.is_pressed("pause"):
            time.sleep(0.2)
            keyboard.wait("pause")
            time.sleep(0.2)

        # 8111/state 返回的值更精确
        state = session.get('http://127.0.0.1:8111/state').text
        # print(state)
        # when no flaps shown on screen, 8111 will return "flaps, %": 0, as expected
        flaps = int(re.search("flaps, %\": (\d*),", state).group(1))
        # print(flaps)

        # with additional else, we can avoid oscillation change
        if flaps >= 16:
            # press r
            keyboard.press("r")
            continue
        elif flaps <= 14:
            # press f
            keyboard.press("f")
            continue
        else:
            keyboard.release("r")
            keyboard.release("f")
            continue
