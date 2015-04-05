from Structure import Syllable, State, Mixture
def parseLine(line):
    array = map(float, line.split())
    return array

f = open('hmm.txt') 

lines = map(lambda x: x.strip(), f.readlines())
stateNum = 0    #stateNum == total num of states in that syllable
mixNum = 0      # total mixture count
transCnt = 0
sylIdx = -1     #syllable index
stIdx = -1      #state index
numMix = 0      #NUMMIX = Total # of Mixture
mixIdx = -1     #Mixture index
piArr = []
stateList =[]
sylList = [0]*20    # save all syllables

state = State()

i = 0   #used to count TRANSP
cur = 0 #to get mean & variance

for line in lines:
    arr = line.split()
    
    if arr[0].startswith('~h'):
        sound = arr[1][1:-1]
        sylIdx = sylIdx + 1
        syllable = Syllable(sound)               ####create syllable
        syllable.setSylIdx(sylIdx)
        pass
    elif arr[0][0] == '<':
        parsetype = arr[0][1:-1]
        
        if parsetype == 'NUMSTATES':
            stateNum = int(arr[1]) - 2          
            
        elif parsetype == 'NUMMIXES':       #identify the start of a state
            stIdx = stIdx +1
            if(state.setIdx == -1):         #1st state
                state.setIdx(stIdx)            ####create state
            else:
                state = State()
                state.setIdx(stIdx)
                
            mixNum = int(arr[1])                
            
        elif parsetype == 'MIXTURE':        #identify the start of a mixture
            numMix = int(arr[1])
            weight = float(arr[2])
            
            
            if(mixIdx+2 > numMix):
                mixIdx = 0
            if(numMix <= mixNum):
                mixIdx = mixIdx +1             
                continue

        elif parsetype == 'MEAN':
            mixture = Mixture(weight, stIdx, mixIdx)     #create mixture
            cur = 1
            
        elif parsetype == 'VARIANCE':
            cur = 2
            
        elif parsetype == 'TRANSP':
            transCnt = int(arr[1])
            cur = 3
             
        else:
            pass
    else:
        if cur == 3:                            #parse pi & a
            temp = map(float, line.split())
            if i == 0:              #form pi
                piArr = [temp[1], temp[2], temp[3]]
                
                aArr = []                       # aArr = 3*4 array // initialize
                for x in range(transCnt-2):
                    aArr.append([0.0]*(transCnt-1))
                i = i+1
                
            elif (i<transCnt-1):
                for tempI in range(1,5):
                    aArr[i-1][tempI-1] = temp[tempI]
                i = i+1
            else:
                syllable.aArr_Pi(aArr, piArr)
                i = 0
                cur = 0
                
        if mixIdx <= numMix and cur == 1:
            meanArr = parseLine(line)
        elif mixIdx <= numMix and cur == 2:
            varArr = parseLine(line)
            cur = 0
            mixture.setMixData(meanArr, varArr)
            state.mixtures.append(mixture)
            # in a state in one word
            if numMix == mixNum:
                numMix = 0
                syllable.states.append(state)
                sylList[sylIdx] = syllable
        else:   #one mixture in a state
            pass
        
