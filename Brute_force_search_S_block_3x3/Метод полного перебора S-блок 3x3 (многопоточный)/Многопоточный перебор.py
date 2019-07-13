from threading import Thread
import random
from datetime import datetime

import sys
import platform
from subprocess import Popen


# define a command that starts new terminal
if platform.system() == "Windows":
    new_window_command = "cmd.exe /c start".split()
else:  #XXX this can be made more portable
    new_window_command = "x-terminal-emulator -e".split()

randb=bin(random.getrandbits(56))[2:]
while len(str(randb))<56:
    randb="0"+str(randb)

def f():
    t1=datetime.now()
    for key in range(0,2**28):
        key=bin(key)[2:]
        while len(str(key))<56:
            key="0"+str(key)
        print("KEY 1 : "+key)
        if key==randb:
            print("KEY IS FOUND : "+str(key))
            t2=datetime.now()
            t=t2-t1
            print("Time spended : "+str(t))
            break
    t2=datetime.now()
    t=t2-t1
    print("Time spended : "+str(t))

def f_2():
    pass


th_1, th_2 = Thread(target=f), Thread(target = f_2)

if __name__ == '__main__':
    th_1.start(), th_2.start()
    th_1.join(), th_2.join()
