#!/usr/local/bin/python

import subprocess
import time
import pandas as pd
import numpy as np
from poloniex import Poloniex
import pdb

class RainPlayer():

    def __init__(self, background, thunder):
        self.background = background
        self.thunder = thunder
        self.PAIR = "USDT_BTC"
        self.ONEDAY = 86400 
        self.PERIOD_LENGTH = 60
        self.TIMEOUT = 10

    def run(self):
        self._calculate_buckets()
        self._play_sound(self.background, 0.3)
        print "starting"
        while(True):
            start_time = time.time()
            orders = self._get_orders(self.PERIOD_LENGTH)
            if orders is not None:
                print "orders"
                self._play_lightning(orders)
            else:
                print "No orders"
            length = int(self.PERIOD_LENGTH - (time.time() - start_time))
            if length > 0:
                time.sleep(length)
            
    def _calculate_buckets(self):
        trades = self._get_orders(self.ONEDAY)
        self.mean = trades.mean()
        deviation = trades.std() 
        self.max = deviation *2 
        

    def _get_orders(self, minutes):
        start_time = time.time() - minutes
        polo = Poloniex(self.TIMEOUT)
        try:
            temp = polo.marketTradeHist(self.PAIR, start_time, time.time())
            df = pd.DataFrame(temp)
            print df.head()
            if len(df) > 0:
                return pd.to_numeric(pd.Series(df["amount"]))
            else:
                return None
        except requests.exceptions.Timeout:
            print "Timeout occurred"
            return None
        

    def _play_lightning(self, orders):
        total = len(orders)
        for order in orders:
            volume = order / self.max
            self._play_sound(self.thunder, volume)
            print str(volume)
            time.sleep(self.PERIOD_LENGTH /float(total))



    def _play_sound(self, filename, volume):
        command = 'afplay {} -v {}'.format(filename, volume)
        print command
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)




if __name__ == '__main__':
    rp = RainPlayer('rain.mp3', 'thunder.mp3')
    rp.run()
