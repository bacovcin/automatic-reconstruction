from copy import deepcopy as copy
from math import ceil
from math import log2 as log
from random import randint, choice
from phon import *
import sys

class cognateSet(object):
    def __init__(self):
        """Cognate sets have a list of cognates, non-cognate score,
           counts for lang1 and lang2 segments and total number of segment
           pairs"""
        self.noncognates = 0
        self.cogdict = {}
        self.lang1dict = {}
        self.lang2dict = {}
        self.totfreq = 0

    def __add__(self,cs2):
        """Combine two cognate sets by copying one and then adding in all
           the features of the second"""
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
        """Calcuate the mutual information of the current language 1 and
           language 2 cognations"""
        score = 0
        for key1 in self.cogdict:
            for key2 in self.cogdict[key1]:
                pxy = self.cogdict[key1][key2]/self.totfreq
                px = self.lang1dict[key1]/self.totfreq
                py = self.lang2dict[key2]/self.totfreq
                score += (pxy*(log(pxy)-(log(px)+log(py))))
        try:
            return log(self.totfreq)-score
        except:
            return 0

    def evaluate(self):
        """Calculate the score of a cognate set: noncognate score +
           confusability score + phonology score"""
        score = self.noncognates * noncognateweight
        score += (self.calcMI() *
                  confusabilityweight)
        for key1 in self.cogdict:
            for key2 in self.cogdict[key1]:
                score += IPAdict[key1].getScore(IPAdict[key2])
        return score

    def update(self,c1,c2):
        """Add a new pair of segments to the set"""
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
        """Method for printing a cognate set"""
        out = 'Non-Cognates: '+str(self.noncognates)+'; '
        out += 'Total Freq: ' + str(self.totfreq) +'; '
        for key1 in self.cogdict:
            for key2 in self.cogdict[key1]:
                out += key1+':'+key2+'='+str(self.cogdict[key1][key2])+'; '
        return out

    def __eq__(self,cs2):
        """Two cognate sets are equal if they have the same noncognate score,
           and the same segment association counts"""
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
    """Recursive function that finds all alignments between to strings and
       returns the cognate set associated with each alignment"""
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
    """Do pairwise comparison in cases of polymorphy"""
    pairs = []
    for i in range(len(lang1)):
        for word1 in lang1[i]:
            for word2 in lang2[i]:
                pairs.append((word1,word2))
    return pairs

def testPair(pair,coglist):
    """Determine the next cognate set to choose for a pair"""
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
    maxscore = ceil(sum(scores))
    q = randint(0,maxscore)
    if q < minscore:
        return choice([mycogs[i] for i in range(len(mycogs))
                       if scores[i] == minscore])
    else:
        return choice(mycogs)

def printCognates(pairs,curcognates):
    """Print a list of pairs of words and if they are cognate"""
    for i in range(len(pairs)):
        if curcognates[i].noncognates > 0:
            print(pairs[i][0] + ' ~ ' + pairs[i][1] +': Not Cognate')
        else:
            print(pairs[i][0] + ' ~ ' + pairs[i][1] +': Cognate')

if __name__ == '__main__':
    """Main function"""
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
