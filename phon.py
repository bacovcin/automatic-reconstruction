class FeatureBundle(object):
    def __init__(self,mydict):
        validValues = ('0','+','-')
        self.feats = {}
        for feat in mydict:
            if mydict[feat] in validValues:
                self.feats[feat] = mydict[feat]

    def getScore(self,fb2):
        if type(fb2) != FeatureBundle:
            raise TypeError
        else:
            score = 0
            for feat in self.feats:
                try:
                    if self.feats[feat] != fb2.feats[feat]:
                        score += 0
                    else:
                        score += 1
                except KeyError:
                    score += 1
            return score

    def __hash__(self):
        return hash((self.iscons))

noncognateweight = 1
confusabilityweight = 1

IPAdict = {'0':FeatureBundle({'iscons':'0'}),
           'p':FeatureBundle({'iscons':'+'}),
           'b':FeatureBundle({'iscons':'+'}),
           't':FeatureBundle({'iscons':'+'}),
           'd':FeatureBundle({'iscons':'+'}),
           'ʈ':FeatureBundle({'iscons':'+'}),
           'ɖ':FeatureBundle({'iscons':'+'}),
           'c':FeatureBundle({'iscons':'+'}),
           'ɟ':FeatureBundle({'iscons':'+'}),
           'k':FeatureBundle({'iscons':'+'}),
           'g':FeatureBundle({'iscons':'+'}),
           'q':FeatureBundle({'iscons':'+'}),
           'ɢ':FeatureBundle({'iscons':'+'}),
           'ʔ':FeatureBundle({'iscons':'+'}),
           'm':FeatureBundle({'iscons':'+'}),
           'ɱ':FeatureBundle({'iscons':'+'}),
           'n':FeatureBundle({'iscons':'+'}),
           'ɳ':FeatureBundle({'iscons':'+'}),
           'ɲ':FeatureBundle({'iscons':'+'}),
           'ŋ':FeatureBundle({'iscons':'+'}),
           'ɴ':FeatureBundle({'iscons':'+'}),
           'ʙ':FeatureBundle({'iscons':'+'}),
           'r':FeatureBundle({'iscons':'+'}),
           'ʀ':FeatureBundle({'iscons':'+'}),
           'ɾ':FeatureBundle({'iscons':'+'}),
           'ɽ':FeatureBundle({'iscons':'+'}),
           'ɸ':FeatureBundle({'iscons':'+'}),
           'β':FeatureBundle({'iscons':'+'}),
           'f':FeatureBundle({'iscons':'+'}),
           'v':FeatureBundle({'iscons':'+'}),
           'θ':FeatureBundle({'iscons':'+'}),
           'ð':FeatureBundle({'iscons':'+'}),
           's':FeatureBundle({'iscons':'+'}),
           'z':FeatureBundle({'iscons':'+'}),
           'ʃ':FeatureBundle({'iscons':'+'}),
           'ʒ':FeatureBundle({'iscons':'+'}),
           'ʂ':FeatureBundle({'iscons':'+'}),
           'ʐ':FeatureBundle({'iscons':'+'}),
           'ç':FeatureBundle({'iscons':'+'}),
           'ʝ':FeatureBundle({'iscons':'+'}),
           'x':FeatureBundle({'iscons':'+'}),
           'ɣ':FeatureBundle({'iscons':'+'}),
           'χ':FeatureBundle({'iscons':'+'}),
           'ʁ':FeatureBundle({'iscons':'+'}),
           'ħ':FeatureBundle({'iscons':'+'}),
           'ʕ':FeatureBundle({'iscons':'+'}),
           'h':FeatureBundle({'iscons':'+'}),
           'ɦ':FeatureBundle({'iscons':'+'}),
           'ɬ':FeatureBundle({'iscons':'+'}),
           'ɮ':FeatureBundle({'iscons':'+'}),
           'ʋ':FeatureBundle({'iscons':'+'}),
           'ɹ':FeatureBundle({'iscons':'+'}),
           'ɻ':FeatureBundle({'iscons':'+'}),
           'j':FeatureBundle({'iscons':'+'}),
           'ɰ':FeatureBundle({'iscons':'+'}),
           'l':FeatureBundle({'iscons':'+'}),
           'ɭ':FeatureBundle({'iscons':'+'}),
           'ʎ':FeatureBundle({'iscons':'+'}),
           'ʟ':FeatureBundle({'iscons':'+'}),
           'i':FeatureBundle({'iscons':'-'}),
           'y':FeatureBundle({'iscons':'-'}),
           'ɨ':FeatureBundle({'iscons':'-'}),
           'ʉ':FeatureBundle({'iscons':'-'}),
           'ɯ':FeatureBundle({'iscons':'-'}),
           'u':FeatureBundle({'iscons':'-'}),
           'ɪ':FeatureBundle({'iscons':'-'}),
           'ʏ':FeatureBundle({'iscons':'-'}),
           'ʊ':FeatureBundle({'iscons':'-'}),
           'e':FeatureBundle({'iscons':'-'}),
           'ø':FeatureBundle({'iscons':'-'}),
           'ɘ':FeatureBundle({'iscons':'-'}),
           'ɵ':FeatureBundle({'iscons':'-'}),
           'ɤ':FeatureBundle({'iscons':'-'}),
           'o':FeatureBundle({'iscons':'-'}),
           'ə':FeatureBundle({'iscons':'-'}),
           'ɛ':FeatureBundle({'iscons':'-'}),
           'œ':FeatureBundle({'iscons':'-'}),
           'ɜ':FeatureBundle({'iscons':'-'}),
           'ɞ':FeatureBundle({'iscons':'-'}),
           'ʌ':FeatureBundle({'iscons':'-'}),
           'ɔ':FeatureBundle({'iscons':'-'}),
           'æ':FeatureBundle({'iscons':'-'}),
           'ɐ':FeatureBundle({'iscons':'-'}),
           'a':FeatureBundle({'iscons':'-'}),
           'ɶ':FeatureBundle({'iscons':'-'}),
           'ɑ':FeatureBundle({'iscons':'-'}),
           'ɒ':FeatureBundle({'iscons':'-'})}
