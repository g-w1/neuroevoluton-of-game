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
        self.maxrun = 30
    def runmodels(self):
        seed = createSeed()
        for model in range(len(self.runpool)):
            print(f"\n {model}th model \n")
            count = self.runpool[model].run(self.maxrun)
            print(count)
            if self.maxrun < count:
                self.maxrun = count
    def addToGenepool(self):
        self.genepool = []
        for i in range(len(self.runpool)):
            self.runpool[i].runcount = self.runpool[i].runcount**4
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
    for epoch in range(100):
        print('epoch',epoch)
        print('adding to genepool')
        pop.addToGenepool()
        print('adding to runpool')
        pop.addToRunpool()
        print('running models')
        pop.runmodels()
    print(pop.maxrun)