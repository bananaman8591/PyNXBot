# Go to root/test of PyNXBot
import signal
import sys
import json
sys.path.append('../')

from rng import XORSHIFT
from nxbot import BDSPBot

config = json.load(open("../config.json"))
b = BDSPBot(config["IP"])

def signal_handler(signal, advances): #CTRL+C handler
    print("Stop request")
    b.close()

signal.signal(signal.SIGINT, signal_handler)

r = XORSHIFT(b.getSeed())
seed = r.state()
advances = 0
print("Initial Seed")
print(f"S[0]: {seed[0]:08X}\tS[1]: {seed[1]:08X}\nS[2]: {seed[2]:08X}\tS[3]: {seed[3]:08X}")
print()
print(f"Advances: {advances}\n\n")

reachedTarget = False
scrolls = 0
targetAdvances = 0
botFlag = input("Advance until target? (y/n) ")
if botFlag == "y" or botFlag == "Y":
    botFlag = True
    targetAdvances = int(input("Input the target advance: "))
else:
    botFlag = False
print("\n")

while True:
    currSeed = b.getSeed()

    while r.state() != currSeed:
        r.next()
        advances += 1

        if r.state() == currSeed:
            print("Current Seed")
            print(f"S[0]: {currSeed[0]:08X}\tS[1]: {currSeed[1]:08X}\nS[2]: {currSeed[2]:08X}\tS[3]: {currSeed[3]:08X}")
            print()
            print(f"Advances: {advances}\n")

            if not reachedTarget and botFlag and advances >= targetAdvances - 300:
                for i in range(2):
                    b.click("HOME")
                    b.pause(0.2)
                reachedTarget = True

    if not reachedTarget:
        print(f"Pokedex scrolled {scrolls} times\n\n")
        scrolls += 1
        b.click("DRIGHT")
        b.pause(0.2)
