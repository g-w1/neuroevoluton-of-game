
import random
from copy import deepcopy
import keras
import numpy as np
from game_environ import test
from statistics import median
def createSeed():
    return [random.randint(-5,5),random.randint(-2,2),random.randint(14,18),random.randint(12,17)]

def mutate(a):
    if not random.randint(0,3):
        b =random.random()*np.random.standard_normal(a.shape)
        return b+a
    else:
        return a
def normalize(v):
    norm = np.sum(v)
    if norm == 0:
       return v
    return v / norm

class Model:
    def __init__(self,hiddenlayersize,model,show = True):
        self.hiddenlayersize = hiddenlayersize
        self.show=  show
        if not model:
            self.model = keras.models.Sequential([
                keras.layers.Dense(hiddenlayersize,input_shape=(5,), activation='tanh'),
                keras.layers.Dense(1, activation='tanh')
        ])
        else:
            self.model = model
    def return_mutated(self,n):
        mods = []
        for i in range(n-1):
            mods.append(Model(self.hiddenlayersize,self.copy_mutate(),show = self.show))
        mods.append(self)
        return mods
    def predictt(self,input):
        """
        returns the output given an input
        """
        input = np.array([input[0],input[1][0],input[1][1],input[2][0],input[2][1]])
        input = normalize(input)
        
        input = input.reshape(1,5)
        out = self.model.predict(input)#do batches!!!!!!!!!!!
        return out
    def run(self,maxrun):
        all_runs = []
        for i in range(50):
            all_runs.append(test(self.predictt,self.show,createSeed()))
        self.runcount = median(all_runs)
        if self.runcount>maxrun:
            jsonmodel = self.model.to_json()
            with open('model.json','w') as f:
                f.write(jsonmodel)
            self.model.save_weights('model.h5')
            print(f'over {maxrun}',self.runcount)
        return self.runcount
        
    def copy_mutate(self):
        model = keras.models.Sequential([
                keras.layers.Dense(self.hiddenlayersize,input_shape=(5,), activation='tanh'),
                keras.layers.Dense(1, activation='tanh')
        ])
        model.set_weights([mutate(x) for x in deepcopy(self.model.get_weights())])
        modelc = Model(self.hiddenlayersize,model,show=False)
        return modelc

if __name__ == "__main__":
    from population import createSeed
    with open('model.json','r') as f:
        loadmodel = f.read()
    for _ in range(1):
        model = Model(10,keras.models.model_from_json(loadmodel).load_weights('model.h5'),show=True)
        model.run(100)
