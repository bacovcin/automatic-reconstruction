from copy import deepcopy as copy
from math import ceil
from math import log2 as log
from random import randint, choice
from phon import *
import sys

class cognateSet(object):
    def __init__(self):
        self.noncognates = 0
        self.cogdict = {}
        self.lang1dict = {}
        self.lang2dict = {}
        self.totfreq = 0

    def __add__(self,cs2):
        if type(cs2) != cognateSet:
            raise TypeError
        else:
            newcognate = copy(self)
            newcognate.noncognates += cs2.noncognates
            for key1 in cs2.cogdict:
                for key2 in cs2.cogdict[key1]:
                    for i in range(cs2.cogdict[key1][key2]):
                        self.totfreq += 1
                        newcognate.update(key1,key2)
                        try:
                            newcognate.lang1dict[key1] += 1
                        except KeyError:
                            newcognate.lang1dict[key1] = 1
                        try:
                            newcognate.lang2dict[key2] += 1
                        except KeyError:
                            newcognate.lang2dict[key2] = 1
            return newcognate

    def calcMI(self):
        score = 0
        for key1 in self.cogdict:
            for key2 in self.cogdict[key1]:
                pxy = self.cogdict[key1][key2]/self.totfreq
                px = self.lang1dict[key1]/self.totfreq
                py = self.lang2dict[key2]/self.totfreq
                score += (pxy*(log(pxy)-(log(px)+log(py))))
        return log(self.totfreq)-score

    def evaluate(self):
        score = self.noncognates * noncognateweight
        score += (self.calcMI() *
                  confusabilityweight)
        for key1 in self.cogdict:
            for key2 in self.cogdict[key1]:
                score += IPAdict[key1].getScore(IPAdict[key2])
        return score

    def update(self,c1,c2):
        try:
            self.cogdict[c1][c2] += 1
        except KeyError:
            try:
                self.cogdict[c1][c2] = 1
            except KeyError:
                self.cogdict[c1] = {}
                self.cogdict[c1][c2] = 1
        try:
            self.lang1dict[c1] += 1
        except KeyError:
            self.lang1dict[c1] = 1
        try:
            self.lang2dict[c2] += 1
        except KeyError:
            self.lang2dict[c2] = 1
        self.totfreq += 1
        return self

    def __str__(self):
        out = 'Non-Cognates: '+str(self.noncognates)+'; '
        out += 'Total Freq: ' + str(self.totfreq) +'; '
        for key1 in self.cogdict:
            for key2 in self.cogdict[key1]:
                out += key1+':'+key2+'='+str(self.cogdict[key1][key2])+'; '
        return out

    def __eq__(self,cs2):
        if type(cs2) != cognateSet:
            return False
        else:
            for key1 in self.cogdict:
                for key2 in self.cogdict[key1]:
                    try:
                        self.cogdict[key1][key2] == cs2.cogdict[key1][key2]
                    except:
                        return False
            else:
                if self.noncognates == cs2.noncognates:
                    return True

    def __ne__(self,cs2):
        return not __eq__(self,cs2)

def getListOfCognates(str1,str2,curcognate):
    cognates = []
    if len(str1) == 0:
        if len(str2) == 0:
            cognates.append(copy(curcognate))
        else:
            newcognate = copy(curcognate)
            for c in str2:
                newcognate.update('0',c)
            cognates.append(newcognate)
    elif len(str2) == 0:
        if len(str1) == 0:
            cognates.append(copy(curcognate))
        else:
            newcognate = copy(curcognate)
            for c in str1:
                newcognate.update(c,'0')
            cognates.append(newcognate)
    else:
        c1 = str1[0]
        newstr1 = str1[1:]
        outcognates = getListOfCognates(newstr1,str2,
                                        copy(curcognate).update(c1,
                                                                '0'))
        for outcognate in outcognates:
            if outcognate not in cognates:
                cognates.append(outcognate)
        for i in range(len(str2)):
            newcognate = copy(curcognate)
            for c in str2[:i]:
                newcognate.update('0',c)
            outcognates = getListOfCognates(newstr1,str2[i+1:],
                                            newcognate.update(c1,
                                                              str2[i]))
            for outcognate in outcognates:
                if outcognate not in cognates:
                    cognates.append(outcognate)
    return cognates

def createPairs(lang1,lang2):
    pairs = []
    for i in range(len(lang1)):
        for word1 in lang1[i]:
            for word2 in lang2[i]:
                pairs.append((word1,word2))
    return pairs

def testPair(pair,coglist):
    curcog = cognateSet()
    for cog in coglist:
        curcog += cog
    mycogs = [cognateSet()]
    mycogs[0].noncognates += max((len(pair[0]),len(pair[1])))*2
    newcogs = getListOfCognates(pair[0],pair[1],cognateSet())
    for cog in newcogs:
        mycogs.append(cog)
    scores = []
    for cog in mycogs:
        scores.append(cog.__add__(curcog).evaluate())
    minscore = min(scores)
    print('Minscore: ' + str(minscore))
    maxscore = ceil(sum(scores))
    print('Maxscore: ' + str(minscore))
    q = randint(0,maxscore)
    input('q: '+str(q))
    if q < minscore:
        return choice([mycogs[i] for i in range(len(mycogs))
                       if scores[i] == minscore])
    else:
        return choice(mycogs)

def printCognates(pairs,curcognates):
    for i in range(len(pairs)):
        if curcognates[i].noncognates > 0:
            print(pairs[i][0] + ' ~ ' + pairs[i][1] +': Not Cognate')
        else:
            print(pairs[i][0] + ' ~ ' + pairs[i][1] +': Cognate')

if __name__ == '__main__':
    pairs = createPairs([x.rstrip().split(',') for x in open(sys.argv[1])],
                        [x.rstrip().split(',') for x in open(sys.argv[2])])
    curcognates = []
    for pair in pairs:
        curcognates.append(testPair(pair,curcognates))
    for i in range(10):
        for pairnum in range(len(pairs)):
            newcognates = copy(curcognates)
            del newcognates[pairnum]
            curcognates[pairnum] = testPair(pair,newcognates)
    printCognates(pairs,curcognates)
