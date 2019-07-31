import sys

DEBUG = 1
class trivial_pwd:

    words = []
    pwd_string = ""

    def score_from_PW(self,pwd_val):
        self.pwd_string = pwd_val.rstrip()
        pwd_found = False
        for word in self.words:
            if self.pwd_string == word.lower():
                pwd_found = True
                break;

        if pwd_found:
            if DEBUG:
                print "Password found in List\n Score 0 von 10"
            return 0
        else:
            if DEBUG:
                print "Password NOT found in List\n Score 10 von 10"
            return 10


    def trainModelWith(self,words):
        self.words = words
