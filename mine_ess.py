import math
from random import randint, uniform
import sys
import time

import cv2
import numpy as np
import pyautogui as pag

class MineBot(object):
    """
    Rune essence mining bot for the Varrock entrance via Aubury
    """
    def __init__(self):
        pass


    def image_match(self, r, img):
        pag.screenshot('triggers/screenie.png', region=r)
        screen = cv2.imread('triggers/screenie.png')
        template = cv2.imread(img)

        res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        threshold = .80
        loc = np.where(res >= threshold)
        if len(loc[0]) > 0:
            return True

        return False


    def travel_time(self, x2, y2):
        """Calculates cursor travel time in seconds per 240-270 pixels, based on a variable rate of movement"""
        rate = uniform(0.09, 0.15)
        x1, y1 = pag.position()
        distance = math.sqrt(math.pow(x2-x1, 2)+math.pow(y2-y1, 2))

        return max(uniform(.08, .12), rate * (distance/randint(250, 270)))


    def random_wait(self, min=0.25, max=0.50):
        """Waits a random number of seconds between two numbers (0.25 and 0.50 default) to mimic human reaction time"""
        return time.sleep(uniform(min, max))


    def logout(self):
        try:
            self.random_coordinate(pag.locateOnScreen('triggers/logout.png', confidence = .8))
            pag.click()
            break
        except ImageNotFoundException:
            self.random_coordinate(1018, 75, 30, 30)
            pag.click()
        self.random_wait()
        try:
            self.random_coordinate(pag.locateOnScreen('triggers/logout_final.png', confidence = .8))
            pag.click()
            break
        except ImageNotFoundException:
            self.random_coordinate(877, 589, 140, 132)
            pag.click()
        sys.exit('Successful exit')


    def pause(self):
        pass


    def random_coordinate(self, location):
        """Moves cursor to random locaction still above the object to be clicked"""
        x = randint(location[0], location[0]+location[2])
        y = randint(location[1], location[1]+location[3])
        time = self.travel_time(x, y)

        return pag.moveTo(x, y, time)


    def custom_click(self, alt_coord, img):
        try:
            self.random_coordinate(pag.locateOnScreen(img, confidence = .8))
            pag.click()
            break
        except ImageNotFoundException:
            self.random_coordinate(alt_coord)
            pag.click()


    # High-level function to mine ess
    def mine(self, mininglap):
        #end when inv full
        if self.image_match((292, 600, 397, 27), 'triggers/full_inv_message.png'):
                return True
        #Deal with level-up interrupt
        if self.image_match((345, 589, 350, 23), 'triggers/levelup_message.png'):
              #continue mining
              self.random_wait(0.05, 0.1)
              self.custom_click((675, 379, 164, 173), 'triggers/ess_vein.png')
        # Deal with random events interrupt
        #
        #
        #click ess initially
        self.custom_click((675, 379, 164, 173), 'triggers/ess_vein.png')
        self.random_wait(0.05, 0.5)


    # High-level function to bank
    def goto_bank(self, bank_locations, triggers):
        # for location in banking_locations
        #     move cursor over random clickable location  #note this looks like the line in our mine_loop
        #     click
        #     wait some short, random period of time
        #      open bank interface
        #
        # move back to starting location
        order = ['portalout', 'bankbooth', 'depositbutton', 'aubury', 'startlocation']
        waits = [(0.1, 0.2), (0.1, 0.2), (0.1, 0.2), (5, 6), (0.1, 0.2)]
        for i in range(len(order)):
            self.custom_click(bank_locations[order[i]])
            if i in range(4):
                self.wait_for_trigger(triggers[order[i]])
            pag.click()
            self.random_wait(waits[i][0], waits[i][1])


""" ------------------------------------- Execute ------------------------------------- """
if __name__ == '__main__':

    mb = MineBot()

    aubury_img =
    ess_img =
    exit_img = {}
    bank_img =

    bank_locations = {'portalout': ((892, 500, 30, 30), 'triggers/ess_mine_exit.png')
                        , 'bankbooth' #STARTHERE
                        , 'depositbutton'
                        , 'aubury'
                        , 'startlocation'
                        }

    bank_triggers = {'dgdoordown': (1630, 230, 470, 200, 'triggers/enter_mysterious_entrance.png'),
                     'depositbox': (1079, 1086, 500, 200, 'triggers/bank_deposit_box.png'),
                     'depositbutton': (1175, 750, 350, 100, 'triggers/deposit_button_hover.png'),
                     'dgdoorup': (1625, 240, 350, 300, 'triggers/exit_mysterious_door.png')}

    print('Character must be in the NW tile by the SWessence pillar, 1 space south of the unpassable Rcokslide.\n'
          'Also, the up arrow must be pushed as high as possible, and rotation must be the same as on first login.\n'
          'Press Ctrl-F2 to exit.')

    time.sleep(5)

    try:
        lap = 0
        while True:
            start_time = time.time()
            mininglap = 1
            while True:
                full = mb.mine_loop(mininglap)
                if full:
                    break
                mininglap += 1
            mb.bank_loop()
            lap += 1
            laptime = time.time()-start_time
            print("Trip number {tripno} took {time} seconds, which is a {xp} xp/hour and "
                  "{ore} iron ore/hour pace.".format(tripno=lap, time=round(laptime, 2),
                                                    xp=('{0:,.0f}'.format(60 / (laptime / 60) * 28 * 5)),
                                                    ore=('{0:,.0f}'.format(60/(laptime/60)*28))))
    except KeyboardInterrupt:
        sys.exit()
