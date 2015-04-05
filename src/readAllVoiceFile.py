from ReadFile import inputX         #inputX = word from a .txt file
from WordHMM import dictionaryHMM   #dictionary HMM info in .dicHMM
from parseHMM import sylList        #have all info about syllables 
from WordHMM import dicWord
from ReadUnigram import unigram
import math

negativeInf = -100000000000

class newSorted:
    def __init__(self):
        self.newLen = 0
        
    def deleteNum(self, listIn):
        delcnt = 0
        idx = 0
        for i in listIn:
            if(i == negativeInf):
                delcnt = delcnt + 1
        self.newLen = listIn.__len__() - delcnt
        self.newList = [0]*(self.newLen)
        for l in listIn:
            if(l != negativeInf):   
                self.newList[idx] = l
                idx = idx +1
                return self.newList

def findMaxIdx(pList, sortedList):
        
    for maxi in range(sortedList.__len__()):
        if(sortedList[sortedList.__len__()-1 - maxi] == negativeInf):
            continue
        if(pList[maxi] == sortedList[sortedList.__len__()-1-maxi]): #sortedList[sortedList.__len__()-1]):
            return maxi 
        
def findMaxVal(original, sortedL):
    newL = newSorted()
    newL.deleteNum(sortedL)
    newlen = newL.newLen
    if(newlen != 0):
        for maxi in range(original.__len__()):
            if(pList[maxi] == newL.newList[newlen-1]):
                return maxi
    else: return -1

class maxB:
    def __init__(self):
        self.maxb = []
        self.expBMax = 0.0
        
    def setMaxB(self, state_num, dicWord, alphaBefore): 
        for j in range(state_num):          #for exponential sum 
            self.maxb = [0]*state_num
            self.sortb = [0]*state_num
            for i in range(state_num):
                if(alphaBefore[i] != negativeInf):
                    self.maxb[i] = alphaBefore[i] * dicWord.wordHMM[i+1][j+1]
                    self.sortb[i] = alphaBefore[i] * dicWord.wordHMM[i+1][j+1]
        self.sortb.sort()
        self.expBMax = self.maxb[findMaxIdx(self.maxb, self.sortb)-1]#self.sortb[state_num-1]


pList = [0]*12
sortedPList = [0.0]*12
t = inputX.len
inputSeq = inputX.inputArr                  #inputSeq has inputX.len length of [39]vectors
dicIdx = 0
maxbIdx = 0

for dicWord in dictionaryHMM.dicHMM:            #dicWord = one dictionary word's whole HMM
    
    state_num = dicWord.wordHMM[0].__len__()-2  #every word's state length is different
    alphaBefore = [0]*state_num                   
   
    sylB = [0]* (state_num/3)    #identify all syllables
    idx=0
    for w in dicWord.word:
        for syl in sylList:
            if(w == syl.sound):
                sylB[idx] = syl
                idx = idx+1
                break
            
    for state in range(state_num):
        if(dicWord.wordHMM[1][state + 1] == 0):
            alphaBefore[state] = negativeInf
        else:
            alphaBefore[state] = math.log(dicWord.wordHMM[1][state + 1]) + sylB[state/3].states[state%3].logFunctionB(inputSeq[0])

    for t in range(inputSeq.__len__()-1):
        for j in range(state_num):
            alphaCurr = [0.0]*state_num
            alphaCurrSort = [0.0]*state_num
            tempSum = 0
        
            maximumB = maxB()
            maximumB.setMaxB(state_num, dicWord, alphaBefore)
            for i in range(state_num):
                if(maximumB.maxb[i] != negativeInf and maximumB.maxb[i] != 0):
                    tempSum = tempSum + math.exp(maximumB.maxb[i] - maximumB.expBMax)
                else:
                    tempSum = negativeInf
            
            for k in range(state_num):
                if(k == 0): 
                    if(tempSum == negativeInf):
                        alphaCurr[k] = negativeInf
                        alphaCurrSort[k] = negativeInf
                    else:
                        alphaCurr[k] = math.log(maximumB.expBMax) + math.log(tempSum)
                        alphaCurrSort[k] = math.log(maximumB.expBMax) + math.log(tempSum)
                if(alphaCurr[k] == negativeInf): 
                    alphaCurr[k] = negativeInf
                    alphaCurrSort[k] = negativeInf
                else:
                    if(tempSum == negativeInf):
                        alphaCurr[k] = negativeInf
                        alphaCurrSort[k] = negativeInf
                    else:
                        alphaCurr[k] = alphaCurr[k] + math.log(maximumB.expBMax) + math.log(tempSum)
                        alphaCurrSort[k] = alphaCurrSort[k] + math.log(maximumB.expBMax) + math.log(tempSum)
        
        if(alphaCurr[j] != negativeInf):
            alphaCurr[j] = alphaCurr[j] + sylB[j/3].states[j%3].logFunctionB(inputSeq[t+1])
            alphaCurrSort[j] = alphaCurrSort[j] + sylB[j/3].states[j%3].logFunctionB(inputSeq[t+1])
        
        tempAlpha = [0]*state_num
        alphaBefore = [0]*state_num
        for stn in range(state_num):
            alphaBefore[stn] = alphaCurr[stn]
            
    p = 0
    dicLen = dicWord.wordHMM[0].__len__()
    for tm in range(state_num):
        if(alphaCurr[tm] != negativeInf and dicWord.wordHMM[tm+1][dicLen-1] != 0.0):
            alphaCurr[tm] = alphaCurr[tm] * (dicWord.wordHMM[tm+1][dicLen-1])
            alphaCurrSort[tm] = alphaCurrSort[tm] * (dicWord.wordHMM[tm+1][dicLen-1])
    alphaCurrSort.sort()
    maxAlpha = findMaxVal(alphaCurr, alphaCurrSort)
    
    tempP = 0.0
    for p0 in range(state_num):
        if(alphaCurr[p0] != negativeInf and maxAlpha != -1):
            tempP = tempP + math.exp(alphaCurr[p0]-alphaCurr[maxAlpha])
        else:
            tempP = negativeInf
            break
    
    if(tempP == negativeInf):
        p = negativeInf
    else:
        p = math.log(alphaCurr[maxAlpha]) + math.log(tempP)
    
    dicLen = dicWord.wordHMM[0].__len__()
    pList[dicIdx] = p
    sortedPList[dicIdx] = p
    dicIdx = dicIdx + 1
    

for index in range(11):
    if(pList[index] != negativeInf):
        pList[index] = pList[index] + math.log(unigram[index].uni)
        sortedPList[index] = sortedPList[index] + math.log(unigram[index].uni)
    else:
        pList[index] = negativeInf
        sortedPList[index] = negativeInf
if(pList[11] != negativeInf):
    pList[11] = pList[11] + math.log(unigram[11].uni)
    sortedPList[11] = sortedPList[11] + math.log(unigram[11].uni)
else:
    pList[index] = negativeInf
    sortedPList[index] = negativeInf
sortedPList.sort()


maxIdx = findMaxVal(pList, sortedPList)
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

print prediction
