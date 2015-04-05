f = open('unigram.txt')

lines = map(lambda x: x.strip(), f.readlines())

unigram =[0]* 12

class Unigram:
    def __init__(self):
        self.word = ''
        self.uni = 0.0
        
    def setUnigram(self, word, uni):
        self.word = word
        self.uni = uni
i = 0
for line in lines:
    arr = line.split()
    u = Unigram()
    u.setUnigram(arr[0], arr[1])
    unigram[i] = u
    i = i+1