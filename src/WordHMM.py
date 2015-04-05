from Dictionary import Dictionary, Word
from parseHMM import sylList

class DictionaryHMM:
    def __init__(self):
        self.dicHMM = [0]*12       #list of OneWord
        
class OneWord:
    def __init__(self):
        self.word = ''
        self.wordSylIdx = []
        self.wordHMM = []
        
    def setHMM(self, word, wordHMM):
        self.word = word
        self.wordHMM = wordHMM
        self.stateNum = wordHMM.__len__() - 2
        
class WholeHMM:
    def ___init__(self, hmm):
        self.word = ''
        self.hmm = []
            
    def setHMM(self, word, hmm):                #HMM syllable
        self.word = word
        self.hmm = hmm
        self.hmmLen = hmm.__len__()
        
        self.wordHMM = []                       #one big vector for whole word hmm
        if(self.hmmLen != 0):
            for index in range((3*self.hmmLen) +2):
                self.wordHMM.append([0.0]*((3*self.hmmLen) + 2))
        self.sylFromHMM = [0]*(hmm.__len__())
        for i in range(hmm.__len__()):
            for j in sylList:
                if(hmm[i] == j.sound):
                    self.sylFromHMM[i] = j
            
f = open('dictionary.txt')
lines = map(lambda x: x.strip(), f.readlines())

dictionaryHMM = DictionaryHMM()                         # all HMM for each word is saved in .dicHMM
dic = Dictionary()         

def createWholeHMM(wordHmm, hmm):
    len = hmm.__len__()
    cnt = 1
    k = 0
    wordHmm[0][1] = (hmm[0].getPi())[0]
    for i in range(0, len*3):
        for j in range(3):
            #wordHmm[i+1][(i*(k/3))+(j+1)] = (hmm[i/3].getAArr())[cnt-1][j]
            if(i/3 == 0):  
                wordHmm[i+1][(i*(k/3))+(j+1)] = (hmm[i/3].getAArr())[cnt-1][j]
            elif i/3 >= 1:
                wordHmm[i+1][(i/3)*3 + (j+1)] = (hmm[i/3].getAArr())[cnt-1][j]
        cnt = cnt + 1
        k = k+1
            
        if(cnt == 4):
            wordHmm[i+1][3*((i+1)/3)+1] = (hmm[i/3].getAArr())[2][3] 
            cnt = 1
            
    return wordHmm 
        
i = 0      
for line in lines:
    w = Word()
    w.setAttribute(line)
    dic.addWord(w.word, w.hmm)
    dicWord = WholeHMM()                   #WholeHMM create
    dicWord.setHMM(w.word, w.hmm)
    
    dictionaryWord = OneWord()
    dictionaryWord.setHMM(w.hmm, createWholeHMM(dicWord.wordHMM, dicWord.sylFromHMM))
    dictionaryHMM.dicHMM[i] = dictionaryWord
    
    i = i+1