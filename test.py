import numpy as np

'''
module for testing
'''

from datetime import datetime
from threading import Timer

x=datetime.today()
y=x.replace(day=x.day, hour=16, minute=47, second=0, microsecond=0)
delta_t=y-x

secs=delta_t.seconds+1

def start_prg():
    print("Start programm")

t = Timer(secs, start_prg)
t.start()