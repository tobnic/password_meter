#
#
# Libary for a Higher Markov Chain Structure
#
# Tobias Nickl
#
# 06.01.2017
#
# OTH - Amberg
#


from math import log, tanh
from itertools import tee, islice, chain, izip

DEBUG = 0
STATS = 0
MARKOV_NOT_FOUND_CRF = 0.1


class higher_structure:
    
    password_probability = 1.0
    pwd_string = ""
    score_normalization_ugh = 180
    score_normalization_ugh = float(3)/2
    
    hSM = {}
    lPM = {}
    
    pw_hSM = {}
    pw_lPM = {}
    
    subsequenceTransmitionFactors = []
    letterTransmitionFactors = []
    
    
    def trainModelWith(self, ugh, ogh, words):
        
        self.score_normalization_ugh = ugh
        self.score_normalization_ogh = ogh
        
        self.train_higherStructModelAndLetterProbability(words)

    
    
    def score_from_PW(self,pwd_val):
        
        #reset old values
        self.resetPasswordScore()
        
        #Set Password
        self.pwd_string = pwd_val.rstrip()
        
        #Get Model form Password
        self.train_higherStructModelAndLetterProbability([self.pwd_string],self.pw_hSM,self.pw_lPM)
        
        if DEBUG or STATS:
            print "Password Structure for PW:",self.pwd_string, self.pw_hSM,"\n"
        
        print "\n\n################################\n>>> Password input:'", self.pwd_string, "'\n###############################\n"

        
        for prob in self.lPM:
            if DEBUG:
                print prob,"-er Sub", self.lPM[prob]

        if DEBUG:
            print "\n##### Password:\n"
            print "pwdModel", self.pw_hSM.get(self.pw_hSM.keys()[0]).get(self.pw_hSM.get(self.pw_hSM.keys()[0]).keys()[0])['raw']
    
        self.subsTransmitionProbability()
        self.letterTransmitionProbability()
        return self.printStatisticWithScore()
         


    def hampelScoreNormalization (self, value):
        #return 5 * ( tanh(0.01 * (float(value)-180) / float(1.5))+1)
        return 5 * ( tanh(0.01 * (float(value)-self.score_normalization_ugh) / self.score_normalization_ogh)+1)

    def printStatisticWithScore(self):
        
        if DEBUG:
            for a in  sorted(self.hSM.get(str(self.pw_hSM.keys()[0]),{}).items(), key=lambda (k, v): v):
                print a

            for b in self.lPM:
                xxx = self.lPM[b][1]
                print "\nTop 3 of Struct size ", b
                for i in range(1,10):
                    if i == len(xxx.get('c_0').items()):
                        break
                    print "     at Pos 1: (Letter,Amount)", sorted(xxx.get('c_0').items(), key=lambda (k, v): v)[(len(xxx.get('c_0').items())-i)]


        print "Sequenz Transmition Probabilities:"
        numb = 1
        for i in self.subsequenceTransmitionFactors:
            if DEBUG or STATS:
                print "\t ->",i
            numb *= i
        print "--->",-10 * log(float(numb),10)
        numb = 1
        print "Char Transmition Probabilities in Sequenz:"
        for i in self.letterTransmitionFactors:
            if DEBUG or STATS:
                print "\t ->",i
            numb *= i
        print "--->",-10 * log(float(numb),10)

        score = self.password_probability
        scorePoints = -10 * log(float(score),10)
        normalizedScorePoints = self.hampelScoreNormalization(scorePoints)
        print "\n----------- HS Result: ----------- \n"
        print "Score: %.2f" % normalizedScorePoints, " von 10"
        print "Points: ", scorePoints," : (",score,")"
        return normalizedScorePoints


    

    
    # TRAINING FOR THE MODEL
    #
    #
    # creating the higher structure model based on words
    #
    # returns a higher structure modle and a model for the probablilty of a character in a structure
    # based on occurrence and position
    #
    def train_higherStructModelAndLetterProbability(self,words,hSM = 1, lPM = 1):

        probabilityByLetterInSubsequeznModel ={} # e.g. {1 (Struct Size): {1(Struct Position): {'c_0' (Letter at Struct Position): {'1'(Letter Following): 1 (Counter), '2': 1}}}}
        letterModel = {}
        stateArray = []
        filelen = len(words)
        higherStrucutreModel = {}
        #Check each Word - casting by each Char of each Word
        for word in words:
        
            #lowercase for all
            word = word.lower()
            
            #init
            shortStr = ""
            statCounter = 0
            stateArray = []
            let = ""
            letPosCount = {}
            char_index = 0
            
            #for each char
            for previous, item, nxt in self.previous_and_next(enumerate(word)):
                char = item[1]
                next_char = ""
                char_index +=1
                if char.isalpha():
                    let = "l"
                elif char.isdigit():
                    let = "n"
                else:
                    let = "s"


                # BEGIN - Count chars for each Word at each Position for each SS

                if previous is not None:
                    #Add letterModel to probabilityByLetterInSubsequeznModel
                    next_char = previous[1]
                    if stateArray[len(stateArray)-1] != let:
                        next_char = 'c_0'
                        dicta = probabilityByLetterInSubsequeznModel
                        dictb = {len(letterModel):letterModel}
                        if dictb.keys()[0] not in dicta:
                            dicta[dictb.keys()[0]] = dictb[dictb.keys()[0]]
                        else:
                            self.sumDictBToDitcA(dicta[dictb.keys()[0]],dictb[dictb.keys()[0]])
                        letterModel = {}
                        char_index = 1
                else:
                    next_char = 'c_0'
            
            
            
                letterModel[char_index] = { next_char: {char:1}}

                if nxt is None:
                    #Add letterModel to probabilityByLetterInSubsequeznModel
                    dicta = probabilityByLetterInSubsequeznModel
                    dictb = {len(letterModel):letterModel}
                    if dictb.keys()[0] not in dicta:
                        dicta[dictb.keys()[0]] =dictb[dictb.keys()[0]]
                    else:
                        self.sumDictBToDitcA(dicta[dictb.keys()[0]],dictb[dictb.keys()[0]])
                    letterModel = {}
                    char_index = 1
            
                # END - Count chars for each Word at each Position for each SS

            
                if not stateArray or stateArray[len(stateArray)-1] != let:
                    letPosCount[statCounter+1]={let:1}
                    statCounter += 1
                    stateArray.append(let)
                else:
                    letPosCount[statCounter][let] +=1
                shortStr = shortStr + str(let)
    
        #probabilityByLetterInSubsequeznModel[str(statCounter)] = {}
        
            if DEBUG:
                print shortStr, statCounter,letPosCount
            
            if str(statCounter) in higherStrucutreModel:
                if shortStr in higherStrucutreModel[str(statCounter)]:
                    higherStrucutreModel[str(statCounter)][shortStr]['raw'] = letPosCount
                    higherStrucutreModel[str(statCounter)][shortStr]['count'] += 1
                else:
                    higherStrucutreModel[str(statCounter)][shortStr] = {'count':1,'raw':letPosCount}
            else:
                higherStrucutreModel[str(statCounter)]={shortStr:{'count':1,'raw':letPosCount}}
        if hSM == 1:
            self.hSM = higherStrucutreModel
        else:
            self.pw_hSM = higherStrucutreModel
        
        if lPM == 1:
            self.lPM = probabilityByLetterInSubsequeznModel
        else:
            self.pw_lPM = probabilityByLetterInSubsequeznModel

    #
    # SUBSEQUENZ TRANSMITION PROBABILITY
    #
    def subsTransmitionProbability(self):
        search_HigherOrder = self.pw_hSM.keys()[0]
        if DEBUG:
            print "\n##### Search - Subsequence Transmition Probability\n"
        for k in self.pw_hSM.get(self.pw_hSM.keys()[0]).get(self.pw_hSM.get(self.pw_hSM.keys()[0]).keys()[0])['raw']:
            search_Pos = k-1
            search_Pos2 = k
    
            search_PosLetter=''
            search_PosLetterLen = 0
            _model = self.pw_hSM.get(self.pw_hSM.keys()[0]).get(self.pw_hSM.get(self.pw_hSM.keys()[0]).keys()[0])['raw'].get(k-1)
            if _model:
                search_PosLetter = _model.keys()[0]
                search_PosLetterLen = _model[search_PosLetter]

    
            search_PosLetter2 = ''
            search_PosLetterLen2 = 0
            _model = self.pw_hSM.get(self.pw_hSM.keys()[0]).get(self.pw_hSM.get(self.pw_hSM.keys()[0]).keys()[0])['raw'].get(k)
            if _model:
                search_PosLetter2 = _model.keys()[0]
                search_PosLetterLen2 = _model[search_PosLetter2]



            #Counter
            count = 0
            count_hs_amount = 0


            #Probabilty of a single letter in a pos
            if search_Pos == 0:
                s_p = search_Pos2
                s_PL = search_PosLetter2
                s_PLL = search_PosLetterLen2
                for i in self.hSM.get(str(search_HigherOrder)) or []:
                    count_hs_amount +=self.hSM[str(search_HigherOrder)][i]['count']
                    for j in self.hSM[str(search_HigherOrder)][i]['raw'].get(s_p) or []:
                        if j == s_PL:
                            if self.hSM[str(search_HigherOrder)][i]['raw'][s_p][j] == s_PLL:
                                count +=self.hSM.get(str(search_HigherOrder)).get(i).get('count')

            #Probabilty of a single letter in a pos following another one
            else:
                s_p = search_Pos
                s_PL = search_PosLetter
                s_PLL = search_PosLetterLen
                for i in self.hSM.get(str(search_HigherOrder)) or []:
                    count_hs_amount +=self.hSM[str(search_HigherOrder)][i]['count']
                    for j in self.hSM[str(search_HigherOrder)][i]['raw'].get(s_p) or []:
                        if j == s_PL:
                            if self.hSM[str(search_HigherOrder)][i]['raw'][s_p][j] == s_PLL:
                                if self.hSM.get(str(search_HigherOrder)).get(i).get('raw').get(search_Pos2).get(search_PosLetter2) == search_PosLetterLen2:
                                    count +=self.hSM.get(str(search_HigherOrder)).get(i).get('count')

            try:
                prob_value = float(count) / float(count_hs_amount)
        
                self.password_probability *= prob_value if prob_value != 0 else MARKOV_NOT_FOUND_CRF
                self.subsequenceTransmitionFactors.append(prob_value if prob_value != 0 else MARKOV_NOT_FOUND_CRF)

            except ZeroDivisionError:
                self.password_probability *= MARKOV_NOT_FOUND_CRF
                self.subsequenceTransmitionFactors.append(MARKOV_NOT_FOUND_CRF)


    #
    # CHAR TRANSMITION PROBABILITY IN A SUBSEQUENZ
    #
    def letterTransmitionProbability(self):
        if DEBUG:
            print "\n##### Search - Letter Transmition Probability in Subsequence \n"
        _model = self.pw_hSM.get(self.pw_hSM.keys()[0]).get(self.pw_hSM.get(self.pw_hSM.keys()[0]).keys()[0])['raw']
        start = 0
        counter_probLetterInPosAmount = 0
        for k in _model:
            struct_size = _model[k].get(_model[k].keys()[0])
            counter_probLetterInPosAmount = 0
            for l in range(0,struct_size):
                pwd_char = self.pwd_string[start:][l]
        
                #Start
                if l == 0:
                    prev_pwd_char = 'c_0'
                else:
                    prev_pwd_char = self.pwd_string[start+l-1]

        
                #is alpha, digit or symbol ?
                if counter_probLetterInPosAmount == 0:
                    if pwd_char.isalpha():
                        for m in self.lPM.get(struct_size,{}).get(l+1,{}).get(prev_pwd_char,{}):
                            if m.isalpha():
                                    counter_probLetterInPosAmount += self.lPM[struct_size][l+1][prev_pwd_char][m]
                    elif pwd_char.isdigit():
                        for m in self.lPM.get(struct_size,{}).get(l+1,{}).get(prev_pwd_char,{}):
                            if m.isdigit():
                                    counter_probLetterInPosAmount += self.lPM[struct_size][l+1][prev_pwd_char][m]
                    else:
                        for m in self.lPM.get(struct_size,{}).get(l+1,{}).get(prev_pwd_char,{}):
                            if not m.isalpha() and not m.isdigit():
                                    counter_probLetterInPosAmount += self.lPM[struct_size][l+1][prev_pwd_char][m]

                try:
                    prob_value = float(self.lPM.get(struct_size,{}).get(l+1,{}).get(prev_pwd_char,{}).get(pwd_char,0))/counter_probLetterInPosAmount
                    self.password_probability *= prob_value if prob_value != 0 else MARKOV_NOT_FOUND_CRF
                    self.letterTransmitionFactors.append(prob_value if prob_value != 0 else MARKOV_NOT_FOUND_CRF)
                except ZeroDivisionError:
                    self.password_probability *= MARKOV_NOT_FOUND_CRF
                    self.letterTransmitionFactors.append(MARKOV_NOT_FOUND_CRF)
                    if DEBUG:
                        print "None - Zero Div"
                if DEBUG:
                    print start+l,"char: ",pwd_char, "struct: ",struct_size,"pos: ",l+1, "prob: ",self.lPM.get(struct_size,{}).get(l+1,{}).get(prev_pwd_char,{}).get(pwd_char,0),"/",counter_probLetterInPosAmount
            start +=struct_size


    #
    # VAR RESET FOR EACH PASSWORD
    #
    def resetPasswordScore(self):
        self.password_probability = 1.0
        
        self.pw_hSM = {}
        self.pw_lPM = {}
        
        self.subsequenceTransmitionFactors = []
        self.letterTransmitionFactors = []
    

    #
    # ADD / MERGE TWO DICTS INTO ONE
    #
    def sumDictBToDitcA(self, dictA,dictB):
        if dictB.keys()[0] not in dictA:
            dictA[dictB.keys()[0]] =dictB[dictB.keys()[0]]
        else:
            for i in dictA:
                if i in dictB.keys():
                    if dictB[i].keys()[0] not in dictA[i]:
                        dictA[i][dictB[i].keys()[0]] =dictB[i][dictB[i].keys()[0]]
                    else:
                        for j in dictA[i]:
                            if j in dictB[i].keys():
                                dictA[i][j] = { k: dictA[i][j].get(k, 0) + dictB[i][j].get(k, 0) for k in set(dictA[i][j]) | set(dictB[i][j]) }
        return dictA

    #
    # PREVIOUS AND NEXT ITEMS FOR ITERABLE OBJECTS
    #
    def previous_and_next(self,some_iterable):
        prevs, items, nexts = tee(some_iterable, 3)
        prevs = chain([None], prevs)
        nexts = chain(islice(nexts, 1, None), [None])
        return izip(prevs, items, nexts)
