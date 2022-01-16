# Go to root of PyNXBot
import signal
import sys
import json
sys.path.append('../')

from structure import PK8
from nxbot import BDSPBot

config = json.load(open("../config.json"))
b = BDSPBot(config["IP"])

def signal_handler(signal, advances): #CTRL+C handler
    print("Stop request")
    b.close()

signal.signal(signal.SIGINT, signal_handler)

for ii in range(1,3):
    print(f"Slot: {ii}")
    pk8 = PK8(b.readDayCare(ii))
    if pk8.isValid() and pk8.ec() != 0:
        print(pk8.toString())
    else:
        print('Empty\n')

b.close()
