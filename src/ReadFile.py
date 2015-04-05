import os

class WordX():          #class to save one whole word
    def __init__(self):
        self.len = 0
        self.inputArr = []
    def setData(self, length, inputArr):
        self.len = length
        self.inputArr = inputArr
for root, dirs, files in os.walk("./tst", topdown = False):
    for name in files:
        f = open(os.path.join(root,name))
        len = name.__len__()
        realVal = name[len-5]
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
