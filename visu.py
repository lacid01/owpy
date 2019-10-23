import sys
import os
from weather import *
import threading
import time

_queu = []
_weatherlist = []
_lock = threading.Lock()

_end = False


def runner():
    while not _end:
        if len(_queu) > 0:
            _lock.acquire()
            k = _queu.pop()
            _lock.release()
            print(k)


def start_visu():
    th = threading.Thread(target=runner())
    th.run()

def add_weather_to_queu(wth):
    _lock.acquire()
    _queu.append(wth)
    _lock.release()

def stop_visu():
    _end = True
