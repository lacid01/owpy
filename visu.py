import sys
import os
from weather import *
import threading
import time
from dbhelper import getWettertableLetzteWerte




class visualisation():

    def __init__(self):

        self.queu = []
        self.weatherlist = {}
        self.lock = threading.Lock()

        self.end = False
        
        print('visualisation: Initialisiere Thread')
        self.updatevisu()
        self.th = threading.Thread( target=self.runner )


    def browsequeu(self):
        while len(self.queu) > 0:
            t = self.queu.pop()
            self.weatherlist[t.city] = t

    def clear_terminal(self):
        if sys.platform == "linux" or sys.platform == "linux2":
           os.system('clear')
        elif sys.platform == "darwin":
            print('OS: OS X')
        elif sys.platform == "win32":
            os.system('cls')

    def runner(self):

        while not self.end:

            self.lock.acquire()
            if len(self.queu) > 0:
                self.browsequeu()
            self.lock.release()

            self.clear_terminal()
            print('Time: ' + str(datetime.now()))

            """
            for cty in self.weatherlist.keys():
                print()
                print(self.weatherlist[cty])
            """
            print("\n")
            try:
                print(self.visudata.to_string(index=False))
            except:
                pass

            time.sleep(0.5)


    def start_visu(self):
        print('Starte Thread')
        self.th.start()
        return True

    def add_weather_to_queu(self, wth):
        self.lock.acquire()
        self.queu.append(wth)
        self.lock.release()

    def stop_visu(self):
        self.end = True
        print('Warte auf join')
        while self.end == False:
            time.sleep(1.0)        
        self.th.join()
        print('Thread beendet')

    def updatevisu(self):
        self.visudata = getWettertableLetzteWerte(hide="True").sort_values(by=['Land','Stadt'])
