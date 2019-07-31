import sys
from math import log, tanh


DEBUG = 0


class adaptive_memory:
    
    password_probability = 1.0
    n = 4
    score_normalization_ugh = 180
    score_normalization_ogh = float(3)/2
    pwd_string = ""
    
    ngrams = {}
    fillDict = []
    
    
    def score_from_PW(self,pwd_val):
        
        self.resetPasswordScore()
        
        #set password
        self.pwd_string = pwd_val.rstrip()
        
        #calculate score
        return self.calculateScore()
        

    def trainModelWith(self,am_n,ugh,ogh,words):
        
        self.n = int(am_n) or self.n
        self.score_normalization_ugh = float(ugh)
        self.score_normalization_ogh = float(ogh)
        
        #init n order Dict for Markov Model
        for i in range(0,self.n):
            self.fillDict.append('c_0')
        
        for word in words:
            word = word.strip().lower()
            self.count_ngrams(self.ngrams,list(word), self.n)
        if DEBUG:
            for i in self.ngrams:
                print "\nauf " + str(i) + " folgt: "
                for j in self.ngrams[i]:
                    if j is not 'sum':
                        print j,float(self.ngrams[i][j])/self.ngrams[i]['sum']*100


    def hampelScoreNormalization (self, value):
        return 5 * ( tanh(0.01 * (float(value)-self.score_normalization_ugh) / self.score_normalization_ogh)+1)

    def calculateScore(self):
        for l in range(0,len(self.pwd_string)+1):
        
            minAMCrCoef = None
            maxAMCrCoef = None
        
            #fill next_letter from pwd
            if l >= len(self.pwd_string):
                next_letter = "('c_e')"
            else:
                next_letter = tuple(self.pwd_string[l])

            #Check Transition probability for:
            t = tuple(self.fillDict)

            #CrCoef needed?
            markovAMTransformation = False

            for mkCount in range(0,self.n+1):
                if t[mkCount:] in self.ngrams and (next_letter) in self.ngrams[t[mkCount:]]:
                    #apply CrCorrection Factor? 
                    if markovAMTransformation:
                        #Looking for maxAMCrCoef
                        for val in  self.ngrams[t[mkCount:]]:
                            if val is not 'sum':
                                poValue = float(self.ngrams[t[mkCount:]][val])/self.ngrams[t[mkCount:]]['sum']
                                if maxAMCrCoef == None or maxAMCrCoef < poValue:
                                    maxAMCrCoef = poValue
                
                        #Correctionfactor right? (Not Zero && CrCoef< 1)
                        if minAMCrCoef != None and maxAMCrCoef != None:
                            CrCoef = minAMCrCoef/maxAMCrCoef
                            if CrCoef < 1.0:
                                self.password_probability *=CrCoef
                                if DEBUG:
                                    print "\t\t\tCrCoef: ",minAMCrCoef,maxAMCrCoef,"->",CrCoef
                            else:
                                if DEBUG:
                                    print "# Warning CrCoef is > 1"
                        else:
                            if DEBUG:
                                print "# Warning CrCoef is None -> do nothing, next round"
                    #Found Transmition -> powd *= pt
                    pt = float(self.ngrams[t[mkCount:]][(next_letter)])/self.ngrams[t[mkCount:]]['sum']*100
                    self.password_probability *= pt/float(100)
                    if DEBUG:
                        print str(t[mkCount:])+" followed by: "+ str((next_letter)),pt,"%"
                    break
                else:
                    markovAMTransformation = True
                    #get Min Value for CrCoef
                    if t[mkCount:] in self.ngrams:
                        for val in  self.ngrams[t[mkCount:]]:
                            if val is not 'sum':
                                poValue = float(self.ngrams[t[mkCount:]][val])/self.ngrams[t[mkCount:]]['sum']
                            
                                if minAMCrCoef == None or minAMCrCoef > poValue:
                                    minAMCrCoef = poValue
                    if DEBUG:
                        print str(t[mkCount:])+" missing ->",next_letter,":"

                    #Unknown letter -> push score
                    if mkCount == self.n and not t[mkCount:]:
                        self.password_probability *=0.01
                        if DEBUG:
                            print "Unknown transmition for Letter -->",next_letter," pwd probability =*0.01"

            #shift all
            for i in range(0,self.n-1):
                self.fillDict[i]=self.fillDict[i+1]
        
            if l == len(self.pwd_string):
                self.fillDict[self.n-1] = 'c_e'
            else:
                #add letter
                self.fillDict[self.n-1] = self.pwd_string[l]
                
        score = self.password_probability
        scorePoints = -10 * log(float(score),10)
        normalizedScorePoints = self.hampelScoreNormalization(scorePoints)
        print "\n----------- AM Result: ----------- \n"
        print "Score: %.2f" % normalizedScorePoints, " von 10"
        print "Points: ", scorePoints," : (",score,")"
        return normalizedScorePoints
    
    
    #
    # VAR RESET FOR EACH PASSWORD
    #
    def resetPasswordScore(self):
        self.password_probability = 1.0
        self.pwd_string = ""
        
        ngrams = {}
        self.fillDict = []
        for i in range(0,self.n):
            self.fillDict.append('c_0')

    def count_ngrams(self,ngrams,tokens, nRange):
        for n in range(0,nRange+1):
            tokens
            for i in range(0,n):
                tokens.insert(0,'c_0')
            if len(tokens) < n:
                return ngrams
            for i in range(len(tokens) - n + 1):
                ngram = tuple(tokens[i:i+n])
                next_letter = tuple(tokens[i+n:i+n+1])
                if not next_letter:
                    next_letter = "('c_e')"
                if ngram not in ngrams:
                    ngrams[ngram]= {}
                    ngrams[ngram]['sum'] = 0
                if next_letter not in ngrams[ngram]:
                    ngrams[ngram][next_letter] = 0
                ngrams[ngram][next_letter] += 1
                ngrams[ngram]['sum'] += 1
            for i in range(0,n):
                tokens.pop(0)

    def merge_counts(self,ngrams_list):
        merged = dict()
        for ngrams in ngrams_list:
            for key, val in ngrams.iteritems():
                if key not in merged:
                    merged[key] = 0
                merged[key] += val
        return merged
