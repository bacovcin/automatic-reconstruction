from copy import deepcopy as copy
from math import ceil
from random import randint
import sys

class FeatureBundle(object):
    def __init__(self,iscons='0'):
        validValues = ('0','+','-')
        if iscons in validValues:
            self.iscons = iscons
        else:
            raise TypeError

    def getScore(self,fb2):
        if type(fb2) != FeatureBundle:
            raise TypeError
        else:
            if self.iscons == fb2.iscons:
                return 0
            else:
                return 1000

    def __hash__(self):
        return hash((self.iscons))

IPAdict = {'0':FeatureBundle('0'),
           'p':FeatureBundle('+'),
           'b':FeatureBundle('+'),
           't':FeatureBundle('+'),
           'd':FeatureBundle('+'),
           'ʈ':FeatureBundle('+'),
           'ɖ':FeatureBundle('+'),
           'c':FeatureBundle('+'),
           'ɟ':FeatureBundle('+'),
           'k':FeatureBundle('+'),
           'g':FeatureBundle('+'),
           'q':FeatureBundle('+'),
           'ɢ':FeatureBundle('+'),
           'ʔ':FeatureBundle('+'),
           'm':FeatureBundle('+'),
           'ɱ':FeatureBundle('+'),
           'n':FeatureBundle('+'),
           'ɳ':FeatureBundle('+'),
           'ɲ':FeatureBundle('+'),
           'ŋ':FeatureBundle('+'),
           'ɴ':FeatureBundle('+'),
           'ʙ':FeatureBundle('+'),
           'r':FeatureBundle('+'),
           'ʀ':FeatureBundle('+'),
           'ɾ':FeatureBundle('+'),
           'ɽ':FeatureBundle('+'),
           'ɸ':FeatureBundle('+'),
           'β':FeatureBundle('+'),
           'f':FeatureBundle('+'),
           'v':FeatureBundle('+'),
           'θ':FeatureBundle('+'),
           'ð':FeatureBundle('+'),
           's':FeatureBundle('+'),
           'z':FeatureBundle('+'),
           'ʃ':FeatureBundle('+'),
           'ʒ':FeatureBundle('+'),
           'ʂ':FeatureBundle('+'),
           'ʐ':FeatureBundle('+'),
           'ç':FeatureBundle('+'),
           'ʝ':FeatureBundle('+'),
           'x':FeatureBundle('+'),
           'ɣ':FeatureBundle('+'),
           'χ':FeatureBundle('+'),
           'ʁ':FeatureBundle('+'),
           'ħ':FeatureBundle('+'),
           'ʕ':FeatureBundle('+'),
           'h':FeatureBundle('+'),
           'ɦ':FeatureBundle('+'),
           'ɬ':FeatureBundle('+'),
           'ɮ':FeatureBundle('+'),
           'ʋ':FeatureBundle('+'),
           'ɹ':FeatureBundle('+'),
           'ɻ':FeatureBundle('+'),
           'j':FeatureBundle('+'),
           'ɰ':FeatureBundle('+'),
           'l':FeatureBundle('+'),
           'ɭ':FeatureBundle('+'),
           'ʎ':FeatureBundle('+'),
           'ʟ':FeatureBundle('+'),
           'i':FeatureBundle('-'),
           'y':FeatureBundle('-'),
           'ɨ':FeatureBundle('-'),
           'ʉ':FeatureBundle('-'),
           'ɯ':FeatureBundle('-'),
           'u':FeatureBundle('-'),
           'ɪ':FeatureBundle('-'),
           'ʏ':FeatureBundle('-'),
           'ʊ':FeatureBundle('-'),
           'e':FeatureBundle('-'),
           'ø':FeatureBundle('-'),
           'ɘ':FeatureBundle('-'),
           'ɵ':FeatureBundle('-'),
           'ɤ':FeatureBundle('-'),
           'o':FeatureBundle('-'),
           'ə':FeatureBundle('-'),
           'ɛ':FeatureBundle('-'),
           'œ':FeatureBundle('-'),
           'ɜ':FeatureBundle('-'),
           'ɞ':FeatureBundle('-'),
           'ʌ':FeatureBundle('-'),
           'ɔ':FeatureBundle('-'),
           'æ':FeatureBundle('-'),
           'ɐ':FeatureBundle('-'),
           'a':FeatureBundle('-'),
           'ɶ':FeatureBundle('-'),
           'ɑ':FeatureBundle('-'),
           'ɒ':FeatureBundle('-')}


class cognateSet(object):
    def __init__(self):
        self.noncognates = 0
        self.cogdict = {}

    def __add__(self,cs2):
        if type(cs2) != cognateSet:
            raise TypeError
        else:
            newcognate = cognateSet()
            newcognate.cogdict = copy(self.cogdict)
            newcognate.noncognates = self.noncognates
            newcognate.noncognates += cs2.noncognates
            for key1 in cs2.cogdict:
                for key2 in cs2.cogdict[key1]:
                    for i in range(cs2.cogdict[key1][key2]):
                        newcognate.update(key1,key2)
            return newcognate

    def evaluate(self):
        score = self.noncognates
        for key1 in self.cogdict:
            for key2 in self.cogdict[key1]:
                score += 1
                score += IPAdict[key1].getScore(IPAdict[key2])/self.cogdict[key1][key2]
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
        return self

    def __str__(self):
        out = 'Non-Cognates: '+str(self.noncognates)+'; '
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
    maxscore = ceil(sum(scores))
    print(scores)
    newscores = [maxscore/x for x in scores]
    newmax = ceil(sum(newscores))
    q = randint(0,newmax)
    for i in range(len(newscores)):
        q -= newscores[i]
        if q < 0:
            break
    return mycogs[i]

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
