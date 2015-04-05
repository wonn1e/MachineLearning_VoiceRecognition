import math

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

def calNorDis(x, mean, var):
    result = 0
    for i in range(39):
        result = result + ((x[i]-mean[i])**2)/var[i] 
    result = -(result/2)
    return result

class Mixture:
    def __init__(self, weight, stateNum, mixNum):
        self.meanVec = []
        self.varVec = []
        self.sdVec = [0.0]*39
        self.stateNum = stateNum
        self.mixNum = mixNum
        self.weight = weight
        self.bResult = 0
        
    def setMixData(self, meanVec, varVec):
        self.meanVec = meanVec
        self.varVec = varVec
        for i in range(0, 39):
            self.sdVec[i] = math.sqrt(varVec[i])
        
class State:
    def __init__(self):
        self.mixtures = []
        self.stateIdx = -1
        
    def setIdx(self, stateIdx):
        self.stateIdx = stateIdx
        
    def functionB(self, inputX):        #input is [39]vector
        mixLen = self.mixtures.__len__()
        self.cal = 1
        temp = {}
        if(mixLen != 0):
            for g in range(mixLen):
                for sd in self.mixtures[g].sdVec:
                    self.cal = self.cal * sd                    
                temp[g] = eln((eexp(calNorDis(inputX, self.mixtures[g].meanVec, self.mixtures[g].varVec)) * (self.mixtures[g].weight) )/(math.sqrt(2*math.pi) *self.cal))                       
                self.cal = 1
        result = 20000
        for g in range(mixLen):
            result = elnsum(result, temp[g])
        #if result == 0: print "zero"
        return result
    
    def logFunctionB(self, inputX):
        mixLen = self.mixtures.__len__()
        logResult = 0.0
        self.cal = 1
        tempSD = 1.0
        tempExp = 0.0
        for g in range(mixLen):
            for inp in range(39):
                tempSD = tempSD * self.mixtures[g].sdVec[inp]
                tempExp = tempExp + ((inputX[inp] - self.mixtures[g].meanVec[inp])**2)/(self.mixtures[g].varVec[inp])
                
            logResult = logResult - 1/math.sqrt((math.pi * 2)) + self.mixtures[g].weight -1/tempSD -tempExp/2
            
            tempExp = 0.0
            tempSD = 1.0
        return logResult
        
            
class Syllable:
    def __init__(self, snd):
        self.sylIdx = 0
        self.states = []
        self.sound = snd
    def setSylIdx(self, idx):
        self.sylIdx = idx
    def aArr_Pi(self, aArr, pi):
        self.aArr = aArr
        self.pi = pi
   
    def getPi(self):
        return self.pi
    def getAArr(self):
        return self.aArr
