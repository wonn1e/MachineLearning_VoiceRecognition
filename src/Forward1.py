import math
from WordHMM import dictionaryHMM   #dictionary HMM info in .dicHMM
from parseHMM import sylList        #have all info about syllables 
from ReadUnigram import unigram
import os

class Result:
    def __init__(self):
        self.result = [0]*11
        for x in range(11):
            self.result[x] = [0]*11
        
    def setResult(self, real, mine):
        self.result[real][mine] = self.result[real][mine] + 1
    
    def getResult(self, idx):
        return self.result[idx]

class WordX():          #class to save one whole word
    def __init__(self):
        self.len = 0
        self.inputArr = []
    def setData(self, length, inputArr):
        self.len = length
        self.inputArr = inputArr

def eexp(x):
    if(x == 20000): #x == 0
        return 0
    else:
        return math.exp(x)
def eln(x):
    if(x == 0):
        return 20000
    elif(x > 0):
        return math.log(x)
 

def elnsum(eln_x, eln_y):
    if eln_x == 20000 or eln_y == 20000:
        if(eln_x == 20000):
            return eln_y
        else:
            return eln_x
    else:
        if(eln_x > eln_y):
            return eln_x + eln(1 + eexp(eln_y - eln_x))
        else:
            return eln_y + eln(1 + eexp(eln_x - eln_y))
            
def elnproduct(eln_x, eln_y):
    if eln_x == 20000 or eln_y ==20000:
        return 20000
   
    return eln_x + eln_y

def findMaxIdx(pList, sortedList):
    for maxi in range(sortedList.__len__()):
        if(pList[maxi] == sortedList[sortedList.__len__()-1]):
            return maxi 
def findRealIdx(realVal):
    if(realVal == 'o'):
        return 0
    elif(realVal == '1'):
        return 1
    elif(realVal == '2'):
        return 2
    elif(realVal == '3'):
        return 3
    elif(realVal == '4'):
        return 4    
    elif(realVal == '5'):
        return 5
    elif(realVal == '6'):
        return 6
    elif(realVal == '7'):
        return 7
    elif(realVal == '8'):
        return 8
    elif(realVal == '9'):
        return 9
    elif(realVal == 'z'):
        return 10

resultMatrix = Result()
for root, dirs, files in os.walk("./tst", topdown = False):
    for name in files:
        f = open(os.path.join(root,name))
        len = name.__len__()
        realVal = name[len-5]
        realIdx = findRealIdx(realVal)
        print "processing %s" % f
        
        inputX = WordX()
        lines = map(lambda x: x.strip(), f.readlines())
        fst_line = lines[0].split()
        length = int(fst_line[0])
        xData = [0]*length
        i = 0
    
        for line in lines:
            i = i+1
            if(i != 1):
                arr = map(float, line.split())
                xData[i-2] = arr
                if(i == length-2):
                    inputX.setData(length, xData)
        ############################
    
        inputSeq = inputX.inputArr
        pList = [0.0]*12
        sortedPList = [0.0]*12
        pIdx = 0
        for dicword in dictionaryHMM.dicHMM:
            state_num = dicword.wordHMM[0].__len__()-2
            alpha_tm1 = [0.0]*state_num
            alpha = [0.0]*state_num
    
            sylB = [0]* (state_num/3)    #identify all syllables
            idx=0
            for w in dicword.word:
                for syl in sylList:
                    if(w == syl.sound):
                        sylB[idx] = syl
                        idx = idx+1
                        break
    
            for i in range(state_num):
                alpha_tm1[i] = elnproduct(eln(dicword.wordHMM[1][i+1]), sylB[i/3].states[i%3].functionB(inputSeq[0]))
        
            for inp in range(inputX.len-1): #t=2 - T
                for j in range(state_num):
                    logalpha = 20000
                    for i in range(state_num):
                        logalpha = elnsum(logalpha, elnproduct(alpha_tm1[i], eln(dicword.wordHMM[i+1][j+1])))
    
                    alpha[j] = elnproduct(logalpha, sylB[j/3].states[j%3].functionB(inputSeq[inp]))
        
                    alpha_tm1 = [0.0]*state_num
                    for k in range(state_num):
                        alpha_tm1[k] = alpha[k]
    
            p = 20000
            for state in range(state_num):
                p = elnsum(p, elnproduct(alpha[state], dicword.wordHMM[state+1][state_num+1]))
            pList[pIdx] = p
            sortedPList[pIdx] = p
    
            pIdx = pIdx + 1
    
        for index in range(11):
            pList[index] = elnproduct(pList[index], float(unigram[index].uni))
            sortedPList[index] = elnproduct(sortedPList[index], float(unigram[index].uni))
        pList[11] = elnproduct(pList[11], float(unigram[10].uni))
        sortedPList[11] = elnproduct(sortedPList[11], float(unigram[10].uni))
        sortedPList.sort()  
    
        maxIdx = findMaxIdx(pList, sortedPList)
        prediction = -1
        
        if(maxIdx == 0):
            prediction = 8
        elif(maxIdx == 1):
            prediction = 5
        elif(maxIdx == 2):
            prediction = 4
        elif(maxIdx == 3):
            prediction = 9
        elif(maxIdx == 4):
            prediction = 0    
        elif(maxIdx == 5):
            prediction = 1
        elif(maxIdx == 6):
            prediction = 7
        elif(maxIdx == 7):
            prediction = 6
        elif(maxIdx == 8):
            prediction = 3
        elif(maxIdx == 9):
            prediction = 2
        elif(maxIdx == 10):
            prediction = 10
        elif(maxIdx == 11):
            prediction = 10
        resultMatrix.setResult(realIdx, prediction)

f1 = open("result.txt", "w")

for a in range(11):
    f1.write(str(resultMatrix.getResult(a)))
f1.close()