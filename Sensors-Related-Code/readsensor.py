import serial
import time
from os import system

passw = 1122
system(f"echo {passw} | sudo -S chmod a+rw /dev/ttyACM0")

# Use For Windows
# ser = serial.Serial('COM7', 115200)

ser = serial.Serial('/dev/ttyACM0', 115200)

time.sleep(1)
failure = False

data = []                       # empty list to store the data
for i in range(5000):
    b = ser.readline()         # read a byte string
    string_n = b.decode()  # decode byte string into Unicode
    # print(string_n)
    string = string_n.rstrip()  # remove \n and \r
    # print(string)
    if "failed" in string:
        # An error has occured in either of the sensors
        failure = True
        break
    if "pulse" in string:
        hb = string.split(" ")[1]
        out_s = f"Heartbeat Value is:- {hb}"
        data.append(out_s)
        print(out_s)
    elif "euler" in string:
        val = string.split(" ")
        out_s = f"Euler Angles in x-y-z dir :- {float(val[1])}, {float(val[2])}, {float(val[3])}"
        print(out_s)
        data.append(out_s)

    elif "aworld" in string:
        val = string.split(" ")
        out_s = f"Acceleration in x-y-z dir :- {float(val[1])}, {float(val[2])}, {float(val[3])}"
        data.append(out_s)
        print(out_s)

    # time.sleep(0.1)            # wait (sleep) 0.1 seconds

ser.close()

with open("out.txt", "w") as f:
    ss = "\n".join(data)
    f.write(ss)
