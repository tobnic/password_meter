import sys
from math import log, ceil

DEBUG = 1
class brute_force:

    N = 52 + 10 + 32 # lower & capital + numbers + special chars
    NoGmax = 100000000 # Guesses per Second
    Tmax = 10 * 365 * 24 * 60 * 60 # years x Days x 24 hours x 60 min x 60 secs
    pwd_string = ""

    def score_from_PW(self,pwd_val):
        
        self.pwd_string = pwd_val.rstrip()
        lmin = log(self.NoGmax*self.Tmax)/log(self.N)
        
        if ceil(lmin) >= len(self.pwd_string):
            if DEBUG:
                print "Password to short (",lmin,") \n Score 0 von 10"
            return 0
        else:
            if DEBUG:
                print "Password len (",lmin,") ok \n Score 10 von 10"
            return 10


    def trainModelWith(self, N = None, NoGmax = None,Tmax = None):
        if N != None:
            self.N = N
                
        if NoGmax != None:
            self.NoGmax = NoGmax
        
        if Tmax != None:
            self.Tmax = Tmax
