from model import Model
import random
import math
import numpy as np
def createSeed():
    return [random.randint(-5,5),random.randint(-2,2),random.randint(14,18),random.randint(12,17)]
class Population(object):
    def __init__(self,number):
        self.number = number
        self.runpool = [Model(random.randint(7,13),False,show=False) for _ in range(number)]
        self.genepool = []
        self.maxrun = 100
    def runmodels(self):
        seed = createSeed()
        for model in self.runpool:
            count = model.run(self.maxrun)
            if self.maxrun < count:
                self.maxrun = count
    def addToGenepool(self):
        self.genepool = []
        for i in range(len(self.runpool)):
            self.runpool[i].runcount = self.runpool[i].runcount**2
        normfactor = sum([model.runcount for model in self.runpool])
        for i in range(len(self.runpool)):
            self.runpool[i].runcount = self.runpool[i].runcount / normfactor
            self.runpool[i].runcount = round(self.runpool[i].runcount * 5 * self.number)
        for model in self.runpool:
            for i in range(model.runcount):
                self.genepool.append(model.copy_mutate())
    def addToRunpool(self): 
        self.runpool = []
        random.shuffle(self.genepool)
        self.runpool = self.genepool[:10]
if __name__ == "__main__":
    pop = Population(100)
    for i in range(10):
        print('epoch',i)
        pop.runmodels()
        pop.addToGenepool()
        pop.addToRunpool()
    print(pop.maxrun)