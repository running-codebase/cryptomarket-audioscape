#!/usr/local/bin/python

import sys
import subprocess
import time
import pandas as pd
import numpy as np
from poloniex import Poloniex

class RainPlayer():

    def __init__(self, pair, background, thunders):
        self.background = background
        self.thunders = thunders
        self.rain_vol = 0.3
        self.thunder_vol = 0.2
        self.PAIR = pair 
        self.ONEDAY = 86400 
        self.PERIOD_LENGTH = 60
        self.TIMEOUT = 10
        self.steps_per_std = 2

    def run(self):
        self._calculate_buckets()
        self._play_sound(self.background, self.rain_vol)
        while(True):
            start_time = time.time()
            orders = self._get_orders(self.PERIOD_LENGTH)
            if orders is not None:
                self._play_lightning(orders)
            length = int(self.PERIOD_LENGTH - (time.time() - start_time))
            if length > 0:
                time.sleep(length)
            
    def _calculate_buckets(self):
        trades = self._get_orders(self.ONEDAY)
        self.mean = trades.mean()
        self.std = trades.std() 

    def _get_orders(self, minutes):
        start_time = time.time() - minutes
        polo = Poloniex(self.TIMEOUT)
        try:
            temp = polo.marketTradeHist(self.PAIR, start_time, time.time())
            df = pd.DataFrame(temp)
            if len(df) > 0:
                return pd.to_numeric(pd.Series(df["amount"]))
            else:
                return None
        except requests.exceptions.Timeout:
            return None
        

    def _play_lightning(self, orders):
        for order in orders:
            step = int((order - self.mean) / (self.std / self.steps_per_std))
            #print "step: " + str(step) + " amount: " + str(order)
            if step <= 0:
                self._play_sound(self.thunders[0], self.thunder_vol)
            elif step < len(self.thunders) -1:
                self._play_sound(self.thunders[step], self.thunder_vol)
            else: #no sound for this step
                self._play_sound(self.thunders[-1], self.thunder_vol)
            time.sleep(self.PERIOD_LENGTH /float(len(orders)))

    def _play_sound(self, filename, volume):
        command = 'afplay {} -v {}'.format(filename, volume)
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)


if __name__ == '__main__':

    if len(sys.argv) < 4:
        print "usage python pair rain_player.py rain.mp3 thunder1.mp3 thunder2.mp3 ..."
        print "minimum of rain audio and one thunder audio required"
        exit()
    else:
        rp = RainPlayer(sys.argv[1], sys.argv[2], sys.argv[3:])
        rp.run()
