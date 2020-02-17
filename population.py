from model import Model
import random
import numpy as np
def createSeed():
    return [random.randint(-10,10),random.randint(-5,5),random.randint(10,30),random.randint(10,20)]
class Population(object):
    def __init__(self,number):
        self.number = number
        self.runpool = [Model(10,False,show=True) for _ in range(number)]
        self.genepool = []
    def runmodels(self):
        seed = createSeed()
        for model in self.runpool:
            model.run(seed)
    def addToGenepool(self):
        self.genepool = []
        normfactor = 1/sum([model.runcount for model in self.runpool])
        for i in range(len(self.runpool)):
            self.runpool[i].runcount /= normfactor
            self.runpool[i].runcount = round(self.runpool[i].runcount * 100)
        for model in self.runpool:
            self.genepool += model.return_mutated(model.runcount)
    def addToRunpool(self): 
        self.runpool = []
        random.shuffle(self.genepool)
        self.runpool = [self.genepool.pop(0) for _ in range(self.number)]
if __name__ == "__main__":
    pop = Population(10)
    pop.runmodels()