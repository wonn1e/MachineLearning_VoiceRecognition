from parseHMM import lines
class Word:
    def __init__(self):
        self.word = ''
        self.hmm = []
    def setAttribute(self, line):
        arr = line.split()
        self.word = arr[0]
        self.hmm = arr[1:]
    
class Dictionary:
    def __init__(self):
        self.words = []
    def addWord(self, word, hmm):
        self.words.append(word)
        self.words.append(hmm)
