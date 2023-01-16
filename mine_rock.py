from random import randint
import pyautogui

def mine_loop():
    for rock in rocks:
        # move cursor over rock in a random clickable location
        # wait for iron to be mineable
        # click
        # wait to have successfully mined the ore
        # wait some short, random period of time
        # move to next rock

def banking_loop():
    # for location in banking_locations
    #     move cursor over random clickable location  #note this looks like the line in our mine_loop
    #     click
    #     wait some short, random period of time
    # move back to starting location

while True:  #run program forever
    while True:  #keep mining until inventory is full
        mine_loop()
        if inventory is full, break out of loop
    banking_loop()
